from pathlib import Path
import re

app = next(Path("appsrc").rglob("package.json")).parent
android = app / "android"
main = next(android.rglob("MainActivity.java"))
source = main.read_text(encoding="utf-8")
match = re.search(r"package\s+([\w.]+);", source)
if not match:
    raise SystemExit("Could not determine Android package from MainActivity")
package = match.group(1)
java_dir = main.parent
plugin = java_dir / "HisabatiPrintPlugin.java"
plugin.write_text("""package ${package};

import android.content.Context;
import android.print.PrintAttributes;
import android.print.PrintManager;
import android.webkit.WebView;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "HisabatiPrint")
public class HisabatiPrintPlugin extends Plugin {
    @PluginMethod
    public void print(PluginCall call) {
        String title = call.getString("title", "Hisabati");
        String format = call.getString("format", "a4");
        getActivity().runOnUiThread(() -> {
            try {
                PrintManager manager = (PrintManager) getContext().getSystemService(Context.PRINT_SERVICE);
                WebView webView = getBridge().getWebView();
                android.print.PrintDocumentAdapter adapter = webView.createPrintDocumentAdapter(title);
                PrintAttributes.MediaSize media = "80mm".equals(format)
                    ? new PrintAttributes.MediaSize("HISABATI_80MM", "80mm", 3150, 11000)
                    : PrintAttributes.MediaSize.ISO_A4;
                PrintAttributes attributes = new PrintAttributes.Builder()
                    .setMediaSize(media)
                    .setResolution(new PrintAttributes.Resolution("hisabati", "Hisabati", 300, 300))
                    .setMinMargins(PrintAttributes.Margins.NO_MARGINS)
                    .build();
                manager.print(title, adapter, attributes);
                call.resolve();
            } catch (Exception e) {
                call.reject("تعذرت تهيئة الطباعة: " + e.getMessage(), e);
            }
        });
    }
}
""".replace("${package}", package), encoding="utf-8")

if "HisabatiPrintPlugin.class" not in source:
    source = source.replace("public class MainActivity extends BridgeActivity {",
        "public class MainActivity extends BridgeActivity {\n    @Override\n    public void onCreate(android.os.Bundle savedInstanceState) {\n        registerPlugin(HisabatiPrintPlugin.class);\n        super.onCreate(savedInstanceState);\n    }")
    main.write_text(source, encoding="utf-8")
print("Registered native Android PrintManager plugin")
