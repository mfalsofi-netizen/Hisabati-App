from pathlib import Path
import re
app=next(Path("appsrc").rglob("package.json")).parent
p=app/"www"/"app.js"
s=p.read_text(encoding="utf-8")
# Remove legacy payment selector handlers: the approved screen has no such control.
s=re.sub(r"function updatePaymentFields\(\)\s*\{.*?\n\}", "", s, count=1, flags=re.S)
s=re.sub(r"^.*\$\(\'paymentStatus\'\)\.addEventListener\([^\n]*\n", "", s, flags=re.M)
p.write_text(s,encoding="utf-8")
print("Removed stale references to the deleted payment-status selector")
