using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerScript : MonoBehaviour {

    public int vLeft;
    public int vRight;
    public int connection1; // 0 = try, 1 = success, -1 = give up
    public int connection2;

    // Use this for initialization
    void Start () {
        connection1 = 0;
        connection2 = 0;
        vLeft = 0;
        vRight = 0;
    }

    // Update is called once per frame
    void Update () {
        float x = Input.GetAxis("Horizontal");
        float y = Input.GetAxis("Vertical");
        vLeft = (int)(255 * (y + x));
        vRight = (int)(255 * (y - x));
        vLeft = Mathf.Max(Mathf.Min(255, vLeft), -255);
        vRight = Mathf.Max(Mathf.Min(255, vRight), -255);
        if (x * x + y * y > 0)
        {
            connection1 = Mathf.Max(connection1, 0);
            connection2 = Mathf.Max(connection2, 0);
        }
    }
}
