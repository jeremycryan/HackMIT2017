// Adapted from https://stackoverflow.com/questions/38816660/sending-data-from-unity-to-raspberry
// and http://answers.unity3d.com/questions/601572/unity-talking-to-arduino-via-wifiethernet.html

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Net.Sockets;
using System;
using System.Net;
using System.Text;

public class CameraFeed : MonoBehaviour {

    TcpListener socket;
    int port = 50000;
    NetworkStream stream;
    TcpListener listener;
    public PlayerScript player;
    TcpClient client;
    StreamWriter writer;
    StreamReader reader;
    int count = 0;
    public Transform wall;
    Wall[] walls = { };

    // Use this for initialization
    void Start () {
    }
	
	// Update is called once per frame
	void Update () {
        connect();
        if (player.connection1 == 1)
        {
            //Read();
            //if (count++ % 5 == 0)
            //{
            Write(player.vLeft + " " + player.vRight);
            //}
        }
    }

    void connect()
    {

        if (player.connection1 == 0)
        {
            try
            {
                print("Start listening");
                listener = new TcpListener(IPAddress.Parse("169.254.130.102"), port);
                listener.Start();
                client = listener.AcceptTcpClient();
                
                stream = client.GetStream();
                print("Trying to connect");
                writer = new StreamWriter(stream);
                reader = new StreamReader(stream);
                player.connection1 = 1;
                print("Connected");
            }
            catch (Exception e)
            {
                Debug.Log("Socket error: " + e);
                player.connection1 = -1;
            }
        }
    }

    void Write(string s)
    {
        writer.Write(s);
        writer.Flush();
    }

    string Read() {
        if (stream.DataAvailable)
        {
            print("hi");
            String s = reader.ReadLine();
            string[] vals = s.Split(' ');
            for(int i = 0; i < int.Parse(vals[0]); i++)
            {
                spawnWall(int.Parse(vals[5*i + 1]),
                    float.Parse(vals[5 * i + 2]),
                    float.Parse(vals[5 * i + 3]),
                    float.Parse(vals[5 * i + 4]),
                    float.Parse(vals[5 * i + 5]));
            }
            return s;
        }
        return "NoData";
    }

    void spawnWall(int type, float x, float y, float z, float theta)
    {
        for(int i=0; i<walls.Length; i++)
        {
            float dx = walls[i].transform.position.x - x;
            float dy = walls[i].transform.position.y - y;
            if(dx*dx+dy*dy<1)
            {
                walls[i].transform.position = new Vector3(x,y,1);
                walls[i].transform.rotation.SetAxisAngle(new Vector3(0,1,0), theta);
                return;
            }
        }
        Transform w = Instantiate(wall);
        w.transform.position = new Vector3(x, y, 1);
        w.transform.rotation.SetAxisAngle(new Vector3(0, 1, 0), theta);

    }
}
