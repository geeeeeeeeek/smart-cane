package projects.ztong.smartcane;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import projects.ztong.smartcane.middleware.USBConnector;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    private void initCameraConnection() {
        CameraImageHandler cameraImageHandler = new CameraImageHandler();
        USBConnector usbConnector = new USBConnector(getApplicationContext(), cameraImageHandler);
    }
}
