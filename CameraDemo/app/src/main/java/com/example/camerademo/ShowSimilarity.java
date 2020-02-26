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
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;
import java.text.NumberFormat;

public class ShowSimilarity extends AppCompatActivity {

    ImageView imageView = null;
    String nameSim= null;
    String path = null;
    String getSim = null;
    String getName = null;

    TextView sim = null;
    TextView name = null;

    Button buttonNo = null;
    Button buttonYes = null;

    private final int HANDLER_MSG_TELL_RECV = 0x124;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_similarity);

        initViews();
        setViews();
    }

    protected void initViews() {
        sim = findViewById(R.id.textView1);
        name = findViewById(R.id.textView2);
        imageView = findViewById(R.id.imageView);
        buttonNo = findViewById(R.id.button_no);
        buttonYes = findViewById(R.id.button_yes);
    }

    protected void setViews() {
        extractString();
//        set the string as its text
        sim.setText(getSim);
        name.setText(getName);
//        display the image
        Bitmap bitmap1 = BitmapFactory.decodeFile(path);
        imageView.setImageBitmap(bitmap1);

        buttonNo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                buttonNoAct();
            }
        });
        buttonYes.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                buttonYesAct();
            }
        });
    }

    protected void extractString() {
//         Get the Intent that started this activity and extract the string
        Intent intent = getIntent();
        path = intent.getStringExtra(MainActivity.EXTRA_PATH);
        nameSim = intent.getStringExtra("result");

//        分离得到名称和相似度
        String[] array = nameSim.split("_");
//        System.out.println(array);
        getName = "name: " + array[0];
        NumberFormat format = NumberFormat.getPercentInstance();
        String s = format.format(Double.parseDouble(array[1]));
        getSim = "similarity: " + s;
    }

    protected void buttonNoAct() {
        Intent intent = new Intent(this, NewUser.class);
        startActivity(intent);
    }

    protected void buttonYesAct() {
        confirmResults();
    }

    protected void confirmResults(){
//        Thread confirm = new Thread()
        final Thread thread = new Thread() {
            public void run(){
                try {
                    Socket tcpCliSocket = new Socket("192.168.31.154", 9999);//host改成服务器的hostname或IP地址
//                    Socket tcpCliSocket = new Socket("10.128.246.101", 9999);
//                    Socket tcpCliSocket = new Socket("193.169.1.107", 9999);
                    DataOutputStream dataOut = new DataOutputStream(tcpCliSocket.getOutputStream());
                    DataInputStream dataIn = new DataInputStream(tcpCliSocket.getInputStream());

//                    发送确认信息
                    sendTextMsg(dataOut, "confirm");
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
            AlertDialog.Builder builder = new AlertDialog.Builder(ShowSimilarity.this);
            builder.setMessage((String)msg.obj);
            builder.setPositiveButton("OK!", new DialogInterface.OnClickListener() {
                @Override
                // what if we click the alert;
                public void onClick(DialogInterface dialog, int which) {
                    startActivity(new Intent(ShowSimilarity.this, MainActivity.class));
                }
            });
            builder.create().show();

        };
    };
}
