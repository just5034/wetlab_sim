using System;
using System.IO;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using JetBrains.Annotations;
using UnityEngine;

/// <summary>
/// Connects to the Python sim over a WebSocket, logs every message it
/// receives to the Console, and sends intents. It holds no sim state.
/// </summary>
public class SimClient : MonoBehaviour
{




    /// <summary>Server address. Editable in the Inspector.</summary>
    [SerializeField] private string url = "ws://127.0.0.1:8765";

    /// <summary>The connection. Null until Start runs.</summary>
    private ClientWebSocket socket;

    /// <summary>Cancelled in OnDestroy to stop any receive still waiting.</summary>
    private CancellationTokenSource cancel;





    /// <summary>
    /// Unity calls this once when Play starts. Create `cancel` and `socket`,
    /// connect to `url`, log "Connected to " + url, then run ReceiveLoop
    /// until the connection ends.
    /// If anything throws: stay silent when `cancel` has been cancelled
    /// (Play mode is stopping). Otherwise log a warning that includes the
    /// exception message and the words "Is the server running?".
    /// </summary>
    private async void Start()
    {

        // creates the 'everybody stop' button and puts it in a field called 'cancel'
        cancel = new CancellationTokenSource();
        // This creates the connection object and stores it in the socket field.
        socket = new ClientWebSocket();

        try
        {
            // ConnectAsync is a built in mehtod in ClientWebSocket that dials the server and waits for it to answer.
            // url is the field "ws://127.0.0.1:8765" and new Uri(url) makes the string into a Uri object which ConnectAsync() expects.
            await socket.ConnectAsync(new Uri(url), cancel.Token);
            Debug.Log("Connected to " + url);

            // This runs the loop to receive server messages.
            await ReceiveLoop(cancel.Token);
        }
        catch (Exception e)
        {

            // cancel.IsCancellationRequested is true if someone calles the Cancel() method on the CancellationTokenSource object.
            if (!cancel.IsCancellationRequested)
            {
                Debug.LogWarning("Lost the sim at " + url + ": " + e.Message + " Is the server running?");
            }
        }
    }





    /// <summary>
    /// While the socket is open, receive one whole message at a time and log
    /// it. When ReceiveMessage returns null, log
    /// "Server closed the connection" and return.
    /// </summary>
    private async Task ReceiveLoop(CancellationToken token)
    {

        /// socket.State can be Open, Closed, or Aborted.
        while (socket.State == WebSocketState.Open)
        {
            string message = await ReceiveMessage(token);

            /// Checking for when the server sends a Close.
            if (message == null)
            {
                Debug.Log("Server closed the connection");
                return;
            }
            Debug.Log("<- " + message);
        }
    }





    /// <summary>
    /// Receive one complete text message and return it as a string.
    /// A message can arrive in several pieces (frames). Keep reading until
    /// a piece arrives with EndOfMessage set to true.
    /// Returns null if the server sent a close message instead.
    /// </summary>
    /// 
    /// async: this method contains await (so it can pause while waiting for the network)
    /// Task<string>: this return type is not just a string, it's a 'Task<string>'. Since the method
    /// is async, it doesn't hand back a string immediately and instead it hands back a Task,
    /// which is a promise that a string will be ready later. If I call it, I write await ReceiveMessage() to wait for the string.
    /// I pass in the cancellation token (token) when I call the method to cancel it when I call OnDestroy.
    private async Task<string> ReceiveMessage(CancellationToken token)
    {
        /// new byte[8192] creates an array of 8192 bytes that are all zero (which is about 8 kilobytes of empty space) to catch one message.
        var buffer = new byte[8192];

        /// a MemoryStream is a growable container of bytes. I write bytes into it and it will scale as needed (python's equivalent is io.BytesIO()) and collects
        /// all pieces of one message in order.
        /// using var just means clean this object up when the method ends. (python equivalent is with ....)
        using var stream = new MemoryStream();

        /// This declares a variable named result of type WebSocketReceiveResult without giving it a value yet.
        WebSocketReceiveResult result;

        do
        {

            /// socket.ReceiveAsync() is build into ClientWebSocket and is a method that waits until the next piece arrives, copies its bytes into
            /// the buffer container and returns a WebSocketReceiveResult describing what happened.
            result = await socket.ReceiveAsync(new ArraySegment<byte>(buffer), token);

            /// result.MessageType says what kind of piece arrived: Text, Binary, or Close.
            /// Close means the server is shutting the connection down. There would be no message to return, so the method returns null.
            /// ReceiveLoop will check for null and log "Server closed the connection" where it is defined.
            if (result.MessageType == WebSocketMessageType.Close)
            {
                return null;
            }


            /// stream.Write(...) copies the bytes that just arrived from buffer into stream.
            /// 0 means start at the beginning of the buffer.
            /// result.Count is how many bytes arrived in this piece.
            stream.Write(buffer, 0, result.Count);
        }
        while (!result.EndOfMessage);

        /// stream.ToArray() gives back all the collected bytes as one byte[] array
        /// and Encoding.UTF8.GetString(...) converts those bytes back into text using UTF-8. Python's equivalent is data.decod("utf-8").
        /// The result is the full message as a string (for example the snapshot JSON string).
        return Encoding.UTF8.GetString(stream.ToArray());
    }





    /// <summary>
    /// Build intent JSON text. For example, BuildIntent("tick", "{\"steps\": 1}")
    /// returns {"type": "intent", "action": "tick", "args": {"steps": 1}}
    /// `argsJson` must already be JSON object text.
    /// </summary>
    public static string BuildIntent(string action, string argsJson)
    {

        string intent = "{\"type\": \"intent\", \"action\": \"" + action + "\", \"args\": " + argsJson + "}";

        return intent;


    }





    /// <summary>
    /// Send one intent. If not connected, log the warning "Not connected" and
    /// return. Otherwise log the JSON, then send
    /// it as one UTF-8 text message. Log before sending, so the Console
    /// shows the request above its reply.
    /// </summary>
    public async Task SendIntent(string action, string argsJson)
    {
        // This is a check to make sure the server is connected (the order of the check matters because
        // if the socket is null and I look for socket.State I'll get a NullReferenceException).
        if (socket == null || socket.State != WebSocketState.Open)
        {
            Debug.LogWarning("Not connected");
            return;
        }

        // This simply constructs the json string (our intent).
        string json = BuildIntent(action, argsJson);
        Debug.Log("-> " + json);

        // This does the opposite of .GetString() in ReceivedMessage; text becomes bytes (the python equivalent is json.encode("utf-8")).
        byte[] bytes = Encoding.UTF8.GetBytes(json);

        // SendAsync (like ReceiveAysync) is built into ClientWebSocket
        // The first argument "new ArraySegment<byte>(bytes)" are the bytes to send in the same wrapper ReceiveAsync used (where it was the bytes to receive).
        // The second is WebSocketMessageType.Text: says this message is text.
        // true: This is EndOfMessage; true signifies that this is the last piece of the message. We are sending the whole message in one piece.
        // cancel.Token: stopping Play can interrupt a send too.
        await socket.SendAsync(new ArraySegment<byte>(bytes), WebSocketMessageType.Text, true, cancel.Token);
    }





    /// <summary>
    /// Send a tick of one step. In Play mode, run it from this component's
    /// three-dot menu in the Inspector.
    /// </summary>
    /// 
    // This square bracketed code indicates an attribute, which is a label that tells Unity something about the method.
    // This one tells Unity: "add a Send tick item to this component's ⋮ menu in the Inspector, and call this method when it's clicked."
    [ContextMenu("Send tick")]
    private async void SendTick()
    {
        await SendIntent("tick", "{\"steps\": 1}");
    }





    /// <summary>
    /// Unity calls this when Play mode stops. Cancel any receive still
    /// waiting, then dispose the socket. Both fields may still be null.
    /// </summary>
    private void OnDestroy()
    {

        /// CancellationTokenSource is a .NET object that works like an "everybody stop" button. Code that waits on the network
        /// is handed a token from this source, and if I call .Cancel(); on the source, every wait holidng that token stops.
        /// 
        /// socket here is a ClientWebSocket object; it is the connection to the python websocket server.
        /// .Dispose(); shuts down the websocket connection and frees what it holds (this shutdown is abrupt).
        
        cancel?.Cancel();
        socket?.Dispose();
        Debug.Log("OnDestroy ran");
    }
}
