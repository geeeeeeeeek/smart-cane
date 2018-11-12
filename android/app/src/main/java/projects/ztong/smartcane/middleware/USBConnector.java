package projects.ztong.smartcane.middleware;

import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.hardware.usb.UsbDevice;
import android.hardware.usb.UsbDeviceConnection;
import android.hardware.usb.UsbManager;
import android.widget.Toast;
import com.felhr.usbserial.UsbSerialDevice;
import com.felhr.usbserial.UsbSerialInterface;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class USBConnector {
    private static final String ACTION_USB_PERMISSION = "projects.ztong.smartcane.USB_PERMISSION";
    private static final Integer ARDUINO_DEVICE_ID = 0x2341;

    private UsbManager usbManager;
    private UsbDevice device;
    private UsbDeviceConnection connection;

    public USBConnector(final Context context, final UsbSerialInterface.UsbReadCallback callback) {
        usbManager = (UsbManager) context.getSystemService(Context.USB_SERVICE);

        HashMap<String, UsbDevice> usbDevices = Objects.requireNonNull(usbManager).getDeviceList();
        // No device connected
        if (usbDevices.isEmpty()) return;

        for (Map.Entry entry : usbDevices.entrySet()) {
            device = (UsbDevice) entry.getValue();
            if (ARDUINO_DEVICE_ID == device.getVendorId()) {
                PendingIntent pi = PendingIntent.getBroadcast(context, 0,
                        new Intent(ACTION_USB_PERMISSION), 0);
                usbManager.requestPermission(device, pi);
                break;
            }
        }

        // Broadcast Receiver to automatically start and stop the Serial connection.
        new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                switch (Objects.requireNonNull(intent.getAction())) {
                    case ACTION_USB_PERMISSION:
                        boolean granted =
                                Objects.requireNonNull(intent.getExtras()).getBoolean(UsbManager.EXTRA_PERMISSION_GRANTED);
                        if (granted) {
                            connection = usbManager.openDevice(device);
                            UsbSerialDevice serialPort = UsbSerialDevice.createUsbSerialDevice(device, connection);

                            if (serialPort == null) {
                                Toast.makeText(context, "PORT IS NULL", Toast.LENGTH_SHORT).show();
                                break;
                            }

                            //Set Serial Connection Parameters.
                            if (serialPort.open()) {
                                serialPort.setBaudRate(9600);
                                serialPort.setDataBits(UsbSerialInterface.DATA_BITS_8);
                                serialPort.setStopBits(UsbSerialInterface.STOP_BITS_1);
                                serialPort.setParity(UsbSerialInterface.PARITY_NONE);
                                serialPort.setFlowControl(UsbSerialInterface.FLOW_CONTROL_OFF);
                                serialPort.read(callback);
                                Toast.makeText(context, "Serial Connection Opened!", Toast.LENGTH_SHORT).show();
                            } else {
                                Toast.makeText(context, "PORT NOT OPEN", Toast.LENGTH_SHORT).show();
                            }
                        } else {
                            Toast.makeText(context, "PERM NOT GRANTED", Toast.LENGTH_SHORT).show();
                        }
                        break;
                    case UsbManager.ACTION_USB_DEVICE_ATTACHED:
                        Toast.makeText(context, "USB DEVICE ATTACHED", Toast.LENGTH_SHORT).show();
                        break;
                    case UsbManager.ACTION_USB_DEVICE_DETACHED:
                        Toast.makeText(context, "USB DEVICE DETACHED", Toast.LENGTH_SHORT).show();
                        break;
                }
            }
        };
    }
}
