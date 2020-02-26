package com.example.camerademo;

import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;

public class NewUser extends AppCompatActivity {

    EditText nameText;
    Button buttonOK;
    private final int HANDLER_MSG_TELL_RECV = 0x124;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_new_user);

        initViews();
        setViews();
    }

    protected void initViews() {
        nameText = findViewById(R.id.editText);
        buttonOK = findViewById(R.id.buttonOK);
    }

    protected void setViews() {
        buttonOK.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String realName = nameText.getText().toString();
                sendUpdateResults(realName);
            }
        });
    }

    protected void sendUpdateResults(final String realName){
        Thread thread = new Thread() {
            public void run(){
                try {
                    Socket tcpCliSocket = new Socket("192.168.31.154", 9999);//host改成服务器的hostname或IP地址
//                    Socket tcpCliSocket = new Socket("10.128.246.101", 9999);
//                    Socket tcpCliSocket = new Socket("193.169.1.107", 9999);
                    DataOutputStream dataOut = new DataOutputStream(tcpCliSocket.getOutputStream());
                    DataInputStream dataIn = new DataInputStream(tcpCliSocket.getInputStream());

//                    发送反馈信息
                    sendTextMsg(dataOut, realName);
                    tcpCliSocket.shutdownOutput();

//                    接收系统反馈信号
                    String feedback = recvMsg(dataIn);

//                    弹框显示成功信息
                    Message msg = handler.obtainMessage(HANDLER_MSG_TELL_RECV, feedback);
                    msg.sendToTarget();

//                    close connection
                    tcpCliSocket.close();

                } catch (UnknownHostException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        };

        thread.start();
    }

    public void sendTextMsg(DataOutputStream out, String msg) throws IOException {
        byte[] bytes = msg.getBytes();
        long len = bytes.length;
        //先发送长度，在发送内容
        out.writeLong(len);
        out.write(bytes);
        out.flush();
    }

    public String recvMsg (DataInputStream dataIn) throws IOException{
        Log.i("TcpClient", "\nstart receiving message");
        byte[] bytes = new byte[1024];
//        String msg = null;
        int n = dataIn.read(bytes); //read应该类似于recv()，有阻塞机制，返回了bytes长度
        System.out.println(n);
        String msg = new String(bytes, 0, n);
        Log.i("TcpClient", "received: " + msg);
        return msg;
    }

    Handler handler = new Handler() {
        public void handleMessage(Message msg) {
            AlertDialog.Builder builder = new AlertDialog.Builder(NewUser.this);
            builder.setMessage((String)msg.obj);
            builder.setPositiveButton("OK!", new DialogInterface.OnClickListener() {
                @Override
                // what if we click the alert;
                public void onClick(DialogInterface dialog, int which) {
                    startActivity(new Intent(NewUser.this, MainActivity.class));
                }
            });
            builder.create().show();

        };
    };


}
