package projects.ztong.smartcane;

import android.widget.Toast;
import com.felhr.usbserial.UsbSerialInterface;

import java.nio.charset.StandardCharsets;

public class CameraImageHandler implements UsbSerialInterface.UsbReadCallback {

    public CameraImageHandler() {

    }

    @Override
    public void onReceivedData(byte[] bytes) {
        String data = new String(bytes, StandardCharsets.UTF_8).concat("/n");
    }
}
