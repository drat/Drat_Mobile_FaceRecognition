package com.example.camerademo;
import com.example.camerademo.ImageTools;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Environment;
import android.view.View;
import android.view.View.OnClickListener;
import android.content.Intent;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ImageView;

import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;

import java.io.BufferedReader;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;

import android.app.Activity;
import android.util.Log;


public class MainActivity extends AppCompatActivity {

    static final int REQUEST_IMAGE_CAPTURE = 1;
    ImageView cameraPic = null;
    ImageView imageView = null;
    String path = null;
    final int SCALE = 10;

    private static final int TCP_SERVER_PORT = 9999;    //should be same to the server port
    public static final String EXTRA_PATH = "com.example.camerodemo.PATH";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initViews();
    }

    private void initViews() {
        imageView = findViewById(R.id.imageView);
        cameraPic = findViewById(R.id.cameraPic);
        cameraPic.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                dispatchTakePictureIntent();
            }
        });
    }

    private void dispatchTakePictureIntent() {
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        intent.putExtra("android.intent.extras.CAMERA_FACING", 1); // 调用前置摄像头
        Uri uri = Uri.fromFile(new File(Environment.getExternalStorageDirectory(),"image.jpg"));
//        获取拍照后未压缩的原图片，并保存在uri路径中，image是一个临时文件，每次拍照后图片都会被替换
        intent.putExtra(MediaStore.EXTRA_OUTPUT, uri);
        startActivityForResult(intent, 1);
    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data) {

        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode != RESULT_OK) {
            return;
        }
        if (requestCode == REQUEST_IMAGE_CAPTURE) {
            // take out the locally saved image and store it in bitmap format
            Bitmap bitmap = BitmapFactory.decodeFile(Environment.getExternalStorageDirectory() + "/image.jpg");
            // compress image
            Bitmap newBitmap = ImageTools.zoomBitmap(bitmap, bitmap.getWidth() / SCALE, bitmap.getHeight() / SCALE);
            // start tcp client thread, transmit newBitmap
            runTcpClient(newBitmap);
            // recycle memory to avoid out of memory error
            bitmap.recycle();

            //将处理过的图片显示在界面上，并保存到本地
            String dir = Environment.getExternalStorageDirectory().getAbsolutePath();
            String filename = String.valueOf(System.currentTimeMillis());
            ImageTools.savePhotoToSDCard(newBitmap, dir, filename);
            path = dir + "/" + filename + ".png";

//            Bitmap bitmap1 = BitmapFactory.decodeFile(path);
//            imageView.setImageBitmap(bitmap1);
        }
    }

    private void runTcpClient(final Bitmap bitmap) {
        Thread thread = new Thread() {
            public void run(){
                try {
//                    Socket tcpCliSocket = new Socket("193.169.1.107", 9999);
                    Socket tcpCliSocket = new Socket("192.168.31.154", 9999);
                    DataOutputStream dataOut = new DataOutputStream(tcpCliSocket.getOutputStream());
                    DataInputStream dataIn = new DataInputStream(tcpCliSocket.getInputStream());

                    sendImgMsg(dataOut, bitmap);
                    // shutdown the output stream to inform the end of the data flow
                    tcpCliSocket.shutdownOutput();
                    // receive the similarity and name returned by the server
                    String predResults = recvMsg(dataIn);
                    // check the results to display the corresponding activities
                    checkResults(predResults);
                    // close connection
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

    public void sendImgMsg(DataOutputStream out, Bitmap bitmap) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        // read bitmap into ByteArrayOutputStream
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, baos);
        // get the size of the data stream
        long len = baos.size();
        byte[] bytes = baos.toByteArray();
        out.writeLong(len); // send data size
        out.write(bytes); // send image data
        Log.i("TcpClient", "sent: " + bytes);
        out.flush();
        // out.close();  一定不能close！tcp是全双工，输出流close会把socket也关闭
    }

    public String recvMsg (DataInputStream dataIn) throws IOException{
        Log.i("TcpClient", "\nstart receiving message");
//        创建这个长度的字节数组
        byte[] bytes = new byte[1024];
//        read应该类似于recv，有阻塞机制，返回了bytes长度
        int n = dataIn.read(bytes);
        System.out.println(n);
//        将字节数组转为String
        String msg = new String(bytes, 0, n);
        Log.i("TcpClient", "received: " + msg);
        return msg;
    }

    protected void checkResults(String predResults){
        if(predResults.equals("new_user")){
            // similarity less than the threshold, open the NewUser activity
            newUser();
        }
        else {
            // activity the ShowSimilarity activity
            showPredResults(path, predResults);
        }
    }

    protected void newUser() {
        Intent intent = new Intent(this, NewUser.class);
        startActivity(intent);
    }

    protected void showPredResults(String picPath, String predResults){
        Intent intent = new Intent(this, ShowSimilarity.class);
        intent.putExtra("result", predResults);
        intent.putExtra(EXTRA_PATH, picPath);    //add value in EditText into intent
        startActivity(intent);
    }



}
