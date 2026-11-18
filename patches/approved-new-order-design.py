from pathlib import Path
import re

app = next(Path("appsrc").rglob("package.json")).parent
hp = app / "www" / "index.html"
jp = app / "www" / "app.js"
h = hp.read_text(encoding="utf-8")
s = jp.read_text(encoding="utf-8")

# Replace the actual New Order markup with real, separate cards.
new_section = r'''<section id="new" class="page hidden">
<div class="approved-order">
<header class="approved-order-head"><span class="head-cart">🛒</span><h2 id="formTitle">طلب جديد</h2><span class="head-menu">☰</span></header>
<input type="hidden" id="editId">
<section class="approved-card customer-card"><div class="customer-grid">
<div class="approved-field"><label for="customerName">اسم العميل　♟</label><input id="customerName" placeholder="اسم العميل"></div>
<div class="approved-field"><label for="customerPhone">رقم الموبايل　☎</label><input id="customerPhone" inputmode="tel" placeholder="رقم الموبايل"><button type="button" class="contact-import-btn" id="pickContact">اختيار من الدليل</button></div>
</div></section>
<section class="approved-card items-card"><div class="approved-card-title"><span>الأصناف　⬡</span><button type="button" class="add-item-btn" id="addItem">＋ إضافة صنف</button></div>
<div class="tablewrap order-items-wrap"><div class="itemline itemline-head"><span>الصنف</span><span>الكمية</span><span>سعر التكلفة</span><span>سعر البيع</span><span>الإجمالي</span><span></span></div><div id="items"></div></div></section>
<section class="approved-card shipping-card"><div class="approved-card-title">تكاليف الشحن　🚚</div><div class="shipping-fields">
<div class="approved-field"><label for="shippingCharge">تكلفة الشحن على العميل</label><input id="shippingCharge" type="number" min="0" step="0.01" value="0"></div>
<div class="approved-field"><label for="shippingCost">تكلفة الشحن الفعلية</label><input id="shippingCost" type="number" min="0" step="0.01" value="0"></div>
</div></section>
<section class="approved-card received-card"><div class="received-label"><label for="amountReceived">المبلغ المستلم　💰</label></div><div class="approved-field"><input id="amountReceived" type="number" min="0" step="0.01" value="0"></div>
<div class="payment-state-field"><label for="paymentStatus">حالة الدفع</label><select id="paymentStatus" class="payment-status"><option value="بانتظار الدفع">بانتظار الدفع</option><option value="تم استلام جزء من المبلغ">تم استلام جزء من المبلغ</option><option value="تم استلام المبلغ بالكامل">تم استلام المبلغ بالكامل</option></select></div></section>
<section class="approved-card summary-card"><div class="approved-card-title summary-title">ملخص الطلب　▦</div><div id="orderSummary" class="notice order-summary"></div></section>
<section class="approved-card currency-card"><label for="currency">العملة</label><select id="currency" class="currency-select"><option value="SAR">🇸🇦 SAR</option><option value="USD">🇺🇸 USD</option><option value="YER">🇾🇪 YER</option></select></section>
<div class="order-form-actions"><button class="btn light" id="clearForm">إعادة تعيين　⟳</button><button class="btn" id="reviewOrder">حفظ الطلب　▣</button></div>
</div></section>
h, n = re.subn(r'<section id="new" class="page hidden">.*?(?=<section id="customers")', new_section + '\n', h, count=1, flags=re.S)
if n != 1:
    raise SystemExit("Could not replace the New Order section markup safely")

css = r"""/* Layout calibrated to the approved mobile reference */
#new{padding:0!important;background:#f5f8ff!important}
#new .approved-order{max-width:520px;margin:0 auto;padding:0 12px 22px;direction:rtl}
#new .approved-order-head{height:58px;margin:0 -12px 10px;padding:0 17px;display:flex;align-items:center;justify-content:space-between;background:linear-gradient(110deg,#1265b6,#07519b);color:#fff;border-radius:0 0 18px 18px}
#new .approved-order-head h2{font-size:23px!important;font-weight:800!important;color:#fff!important;margin:0!important}
#new .head-cart,#new .head-menu{font-size:26px;color:#fff;line-height:1}
#new .approved-card{background:#fff;border:1px solid #cbdcf1;border-radius:15px;margin:0 0 10px;padding:10px;box-shadow:0 2px 7px rgba(30,80,140,.07)}
#new .customer-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
#new .customer-grid>.approved-field+ .approved-field{border-right:1px solid #b9cce5;padding-right:10px}
#new .approved-field{min-width:0}
#new .approved-field label{display:block;font-size:13px;font-weight:800;color:#163a67;margin:0 0 6px}
#new .approved-field input,#new .approved-field select{width:100%;height:39px;box-sizing:border-box;border:1px solid #cbd4e1;border-radius:10px;background:#fbfbfd;padding:7px 10px;font:15px Tahoma,Arial,sans-serif;color:#222;min-width:0}
#new input[type=number]{direction:ltr!important;text-align:center!important;font-variant-numeric:tabular-nums}
#new .contact-import-btn{margin-top:6px;border:0;border-radius:9px;background:#176bc0;color:#fff;padding:7px 10px;font:700 12px Tahoma}
#new .approved-card-title{height:34px;margin:-10px -10px 8px;padding:0 12px;display:flex;align-items:center;justify-content:space-between;background:#dcecff;color:#104d91;border-radius:14px 14px 0 0;font-size:17px;font-weight:800}
#new .add-item-btn{border:0;border-radius:9px;background:#1268bb;color:#fff;padding:6px 12px;font:700 13px Tahoma}
#new .order-items-wrap{overflow-x:auto;margin:0}
#new .itemline{grid-template-columns:minmax(95px,1.55fr) 42px 70px 70px 70px 28px!important;min-width:390px!important;gap:5px!important}
#new .itemline-head{font-size:11px;font-weight:800;color:#16375e;align-items:center;background:#edf5ff;padding:7px 3px;border-radius:7px}
#new .itemline input{height:38px!important;min-height:38px!important;padding:4px!important;font-size:12px!important;border-radius:8px!important}
#new .itemline .iqty{max-width:42px}
#new .itemline .lineTotal{height:38px;display:flex;align-items:center;justify-content:center;background:#e5f0ff;border-radius:8px;color:#1262b4;font-size:12px;font-weight:800;direction:ltr}
#new .shipping-fields{display:grid;grid-template-columns:1fr 1fr;gap:12px}
#new .shipping-fields>.approved-field+ .approved-field{border-right:1px solid #b9cce5;padding-right:10px}
#new .shipping-fields input{height:38px;text-align:center!important}
#new .received-card{display:grid;grid-template-columns:1fr 1.2fr;align-items:center;gap:8px}
#new .received-label{font-weight:800;color:#173b69}
#new .received-label label{font-size:15px}
#new .received-card>.approved-field input{background:#e8f2ff;border-color:#b8d1ef;font-size:17px;font-weight:800}
#new .payment-state-field{grid-column:1/-1;display:flex;align-items:center;gap:10px;padding-top:5px;border-top:1px solid #edf1f6}
#new .payment-state-field label{font-size:12px;font-weight:700;color:#40536a}
#new .payment-state-field select{flex:1;height:34px;border:1px solid #d2dce8;border-radius:8px;background:#fff;padding:5px;font:12px Tahoma}
#new .summary-card{border-color:#b8d2f0}
#new .summary-title{background:#125ca7;color:#fff}
#new #orderSummary{margin:0!important;padding:8px!important;background:#f8fbff!important;border:0!important;border-radius:9px!important}
#new .sum-grid{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:5px!important}
#new .sum-item{min-width:0;padding:8px 4px!important;text-align:center!important;border-left:1px solid #b9cce5!important;background:transparent!important}
#new .sum-item:last-child{border:0!important}
#new .sum-item small{display:block;font-size:10px!important;line-height:1.35;color:#3f4f65!important}
#new .sum-item b{display:block;margin-top:6px;font-size:15px!important;font-weight:800!important;direction:ltr!important;text-align:center!important;white-space:nowrap}
#new .sum-cost b{color:#475569!important}#new .sum-sale b{color:#1266b9!important}
#new .sum-due{background:#fff0d5!important;border-radius:8px!important}#new .sum-due b{color:#a64d00!important}
#new .currency-card{display:flex;align-items:center;gap:15px;padding:8px 12px}
#new .currency-card label{font-size:13px;font-weight:800;color:#233b5b}
#new .currency-select{width:auto;max-width:125px;height:34px!important;font-size:12px!important}
#new .order-form-actions{display:grid;grid-template-columns:1fr 1.25fr;gap:9px;margin:12px 0 0}
#new .order-form-actions button{height:53px;min-height:53px;border-radius:13px;font-size:16px;font-weight:800}
#new #reviewOrder{background:linear-gradient(110deg,#1674d0,#0755a2)!important;color:#fff!important}
#new #clearForm{background:#f5f7fc!important;border:1px solid #9baec8!important;color:#263750!important}
@media(max-width:390px){#new .approved-order{padding-left:8px;padding-right:8px}#new .approved-order-head{margin-left:-8px;margin-right:-8px}#new .sum-item b{font-size:12px!important}#new .sum-item small{font-size:9px!important}#new .customer-grid{gap:7px}}

h = h.replace("</style></head>", css + "\n</style></head>", 1)

# Remove the prior faulty layout helper which attached card classes to the entire form panel.
s = re.sub(r'\nfunction applyApprovedNewOrderLayout\(\)\{.*?window\.addEventListener\(\'load\',applyApprovedNewOrderLayout\);\s*', '\n', s, count=1, flags=re.S)

# Keep English digits in all newly created number fields, including item rows.
s = s.replace("x.lang=(navigator.language||document.documentElement.lang||'ar');", "x.lang='en-US';")
s = s.replace("function applyDeviceNumberLocale(root=document){\n const locale=(navigator.languages&&navigator.languages[0])||navigator.language||document.documentElement.lang||'ar';", "function applyDeviceNumberLocale(root=document){\n const locale='en-US';")
s = s.replace("el.lang=locale;", "el.lang='en-US';")
# Amount received remains visible for all payment states, as previously approved.
s = s.replace("wrap.classList.toggle('hidden',state!=='تم استلام جزء من المبلغ');", "wrap.classList.remove('hidden');")
s = s.replace("$('amountReceived').lang=(navigator.language||document.documentElement.lang||'ar');", "$('amountReceived').lang='en-US';")

hp.write_text(h, encoding="utf-8")
jp.write_text(s, encoding="utf-8")
print("Rebuilt New Order HTML into separate cards and applied matching responsive design")
