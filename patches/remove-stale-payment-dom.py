from pathlib import Path
app=next(Path("appsrc").rglob("package.json")).parent
p=app/"www"/"app.js"
lines=p.read_text(encoding="utf-8").splitlines()
# The new order form intentionally has no paymentStatus DOM element.
# Remove every legacy line that tries to read or listen to that deleted selector.
lines=[line for line in lines if "$('paymentStatus')" not in line]
p.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Removed all legacy DOM access to the deleted payment-status selector")
