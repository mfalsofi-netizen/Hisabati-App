from pathlib import Path
import re

app = Path(".").resolve()
android = app / "android"
main = next(android.rglob("MainActivity.java"))
source = main.read_text(encoding="utf-8")
match = re.search(r"package\s+([\w.]+);", source)
if not match:
    raise SystemExit("Could not determine Android package from MainActivity")
package = match.group(1)
java_dir = main.parent
plugin = java_dir / "HisabatiContactsPlugin.java"
plugin.write_text("""package ${package};

import android.app.Activity;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.provider.ContactsContract;
import com.getcapacitor.ActivityResult;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.ActivityCallback;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "HisabatiContacts")
public class HisabatiContactsPlugin extends Plugin {
    @PluginMethod
    public void pick(PluginCall call) {
        Intent intent = new Intent(Intent.ACTION_PICK, ContactsContract.CommonDataKinds.Phone.CONTENT_URI);
        startActivityForResult(call, intent, "contactPicked");
    }

    @ActivityCallback
    private void contactPicked(PluginCall call, ActivityResult result) {
        if (call == null) return;
        if (result.getResultCode() != Activity.RESULT_OK || result.getData() == null) {
            call.reject("تم إلغاء اختيار جهة الاتصال");
            return;
        }
        Uri uri = result.getData().getData();
        if (uri == null) {
            call.reject("لم يتم اختيار رقم هاتف");
            return;
        }
        String[] projection = {
            ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME,
            ContactsContract.CommonDataKinds.Phone.NUMBER
        };
        try (Cursor cursor = getContext().getContentResolver().query(uri, projection, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) {
                JSObject resultData = new JSObject();
                resultData.put("name", cursor.getString(0));
                resultData.put("phone", cursor.getString(1));
                call.resolve(resultData);
            } else {
                call.reject("تعذر قراءة جهة الاتصال المحددة");
            }
        } catch (Exception e) {
            call.reject("تعذر قراءة جهة الاتصال: " + e.getMessage(), e);
        }
    }
}
""".replace("${package}", package), encoding="utf-8")

if "HisabatiContactsPlugin.class" not in source:
    if "public void onCreate(android.os.Bundle savedInstanceState)" in source:
        source = source.replace(
            "public void onCreate(android.os.Bundle savedInstanceState) {",
            "public void onCreate(android.os.Bundle savedInstanceState) {\n        registerPlugin(HisabatiContactsPlugin.class);"
        )
    else:
        source = source.replace(
            "public class MainActivity extends BridgeActivity {",
            "public class MainActivity extends BridgeActivity {\n    @Override\n    public void onCreate(android.os.Bundle savedInstanceState) {\n        registerPlugin(HisabatiContactsPlugin.class);\n        super.onCreate(savedInstanceState);\n    }"
        )
    main.write_text(source, encoding="utf-8")
print("Registered Android system contact picker plugin")
