// Adapted from https://stackoverflow.com/questions/749964/sending-and-receiving-an-image-over-sockets-with-c-sharp
// and https://stackoverflow.com/questions/26058594/how-to-get-all-data-from-networkstream
// and https://stackoverflow.com/questions/221925/creating-a-byte-array-from-a-stream

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.IO;
using System.Threading;
using System;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;
using UnityEngine.UI;

public class CameraFeed2 : MonoBehaviour {

    TcpListener socket;
    int port = 50001;
    NetworkStream stream;
    public PlayerScript player;
    Texture2D tex;
    StreamWriter writer;
    StreamReader reader;
    TcpListener listener;
    TcpClient client;
    int index = 0;

    void Start()
    {
        
    }

    void Update()
    {
        //connect();
        if (player.connection2!=1||!stream.DataAvailable) return;
        byte[] length = new byte[4];
        stream.Read(length, 0, 4);
        byte[] data = new byte[921600];
        using (MemoryStream ms = new MemoryStream())
        {
            for(int i = 0; i < data.Length; i+=100)
            {
                stream.Read(data, 0, 100);
                ms.Write(data, 0, 100);
            }
            byte[] imageData = ms.ToArray();
            tex.LoadRawTextureData(imageData);
            tex.Apply();

            Vector2 pivot = new Vector2(0.5f, 0.5f);
            Rect tRect = new Rect(0, 0, tex.width, tex.height);
            GetComponent<Image>().overrideSprite = Sprite.Create(tex, tRect, pivot);
            print(index++);
        }
    }

    void connect()
    {
        if (player.connection2 == 0)
        {
            try
            {
                tex = new Texture2D(640, 480, TextureFormat.RGB24, false);
                listener = new TcpListener(IPAddress.Parse("169.254.130.102"), port);
                listener.Start();
                client = listener.AcceptTcpClient();
                stream = client.GetStream();
                player.connection2 = 1;
                print("YAY, YOU CONNECTED!");
            }
            catch (Exception e)
            {
                Debug.Log("Socket error: " + e);
                player.connection2 = -1;
                return;
            }
        }
    }
}
