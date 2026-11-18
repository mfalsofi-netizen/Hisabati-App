from pathlib import Path
import re

app = next(Path("appsrc").rglob("package.json")).parent
hp = app / "www" / "index.html"
jp = app / "www" / "app.js"
h = hp.read_text(encoding="utf-8")
s = jp.read_text(encoding="utf-8")

# Replace the actual New Order markup with real, separate cards.
new_section = r'''<section id="new" class="page hidden">
<div class="order-page-shell">
  <div class="order-page-heading"><div><span class="order-kicker">إدارة المشتريات</span><h2 id="formTitle">طلب جديد</h2></div><span class="order-heading-icon">＋</span></div>
  <input type="hidden" id="editId">

  <section class="order-card customer-section">
    <div class="order-section-heading"><span class="order-section-icon">♙</span><div><h3>بيانات العميل</h3><p>أدخل بيانات العميل أو اختره من دليل الهاتف</p></div></div>
    <div class="customer-fields">
      <div class="order-field"><label for="customerName">اسم العميل</label><input id="customerName" placeholder="اكتب اسم العميل"></div>
      <div class="order-field"><label for="customerPhone">رقم الهاتف</label><input id="customerPhone" inputmode="tel" placeholder="رقم الهاتف"><button type="button" class="contact-import-btn" id="pickContact"><svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 7h6M9 11h6M9 15h3"/></svg> استيراد من دليل الهاتف</button></div>
    </div>
    <div class="currency-field order-field"><label for="currency">عملة الطلب</label><select id="currency" class="currency-select"><option value="SAR">🇸🇦 SAR — ريال سعودي</option><option value="USD">🇺🇸 USD — دولار أمريكي</option><option value="YER">🇾🇪 YER — ريال يمني</option></select></div>
  </section>

  <section class="order-card items-section">
    <div class="order-section-heading"><span class="order-section-icon">▤</span><div><h3>أصناف الطلب</h3><p>أضف المنتجات وحدد الكمية والتكلفة وسعر البيع</p></div></div>
    <div class="tablewrap order-items-wrap"><div class="itemline itemline-head"><span>الصنف</span><span>الكمية</span><span>سعر التكلفة</span><span>سعر البيع</span><span>الإجمالي</span><span></span></div><div id="items"></div></div>
    <button class="add-item-btn" id="addItem" type="button"><svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg> إضافة صنف جديد</button>
  </section>

  <section class="order-card shipping-section">
    <div class="order-section-heading"><span class="order-section-icon">⇄</span><div><h3>تكاليف الشحن</h3><p>حدد تكلفة الشحن الفعلية والمبلغ على العميل</p></div></div>
    <div class="shipping-fields">
      <div class="order-field"><label for="shippingCost">تكلفة الشحن الفعلية</label><input id="shippingCost" type="number" min="0" step="0.01" value="0" placeholder="0.00"><small>ما دفعته لشركة الشحن</small></div>
      <div class="order-field"><label for="shippingCharge">تكلفة الشحن على العميل</label><input id="shippingCharge" type="number" min="0" step="0.01" value="0" placeholder="0.00"><small>ما سيدفعه العميل</small></div>
    </div>
  </section>

  <section class="order-card payment-section">
    <div class="order-section-heading"><span class="order-section-icon">◉</span><div><h3>حالة الدفع</h3><p>حدد حالة المبلغ المستلم من العميل</p></div></div>
    <div class="payment-fields">
      <div class="order-field"><label for="paymentStatus">حالة الدفع</label><select id="paymentStatus" class="payment-status"><option value="بانتظار الدفع">بانتظار الدفع</option><option value="تم استلام جزء من المبلغ">تم استلام جزء من المبلغ</option><option value="تم استلام المبلغ بالكامل">تم استلام المبلغ بالكامل</option></select></div>
      <div class="order-field" id="receivedAmountWrap"><label for="amountReceived">المبلغ المستلم</label><input id="amountReceived" type="number" min="0" step="0.01" value="0" placeholder="0.00"></div>
    </div>
  </section>

  <section class="order-card notes-section"><div class="order-field"><label for="orderNotes">ملاحظات إضافية (اختياري)</label><textarea id="orderNotes" placeholder="أضف أي تفاصيل تخص الطلب..."></textarea></div></section>

  <section class="order-card summary-section">
    <div class="order-section-heading"><span class="order-section-icon">▦</span><div><h3>ملخص الطلب</h3><p>مراجعة إجماليات الطلب قبل الحفظ</p></div></div>
    <div id="orderSummary" class="notice order-summary"></div>
  </section>

  <div class="order-form-actions"><button class="btn" id="reviewOrder"><svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h12l4 4v14H3V3z"/><path d="M7 3v6h10V3M7 21v-8h10v8"/></svg> حفظ الطلب</button><button class="btn light" id="clearForm"><svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 14 4 9l5-5"/><path d="M4 9h9a7 7 0 0 1 0 14h-2"/></svg> إلغاء الطلب</button></div>
</div>
</section>'''
h, n = re.subn(r'<section id="new" class="page hidden">.*?</section>\s*<section id="customers"', new_section + '\n<section id="customers"', h, count=1, flags=re.S)
if n != 1:
    raise SystemExit("Could not replace the New Order section markup safely")

css = r"""
/* Actual card-based New Order screen: scoped to the redesigned page only */
#new{background:#f3f7fc!important}
#new .order-page-shell{width:100%;max-width:720px;margin:0 auto;padding:12px 2px 24px}
#new .order-page-heading{display:flex;align-items:center;justify-content:space-between;margin:2px 2px 15px;padding:2px 4px}
#new .order-kicker{font-size:10px;font-weight:800;letter-spacing:.4px;color:#4382c5}
#new .order-page-heading h2{font-size:22px;font-weight:800;color:#142f50;margin:3px 0 0}
#new .order-heading-icon{width:43px;height:43px;border-radius:14px;background:#e4f0ff;color:#1769b5;display:grid;place-items:center;font-size:25px;font-weight:400}
#new .order-card{background:#fff;border:1px solid #e1eaf5;border-radius:17px;padding:15px;margin:0 0 13px;box-shadow:0 4px 15px rgba(22,57,96,.055)}
#new .order-section-heading{display:flex;align-items:center;gap:10px;margin:0 0 13px;padding:0 0 11px;border-bottom:1px solid #edf2f8}
#new .order-section-heading h3{font-size:15px;color:#193c63;font-weight:800;margin:0 0 3px}
#new .order-section-heading p{font-size:10px;color:#8090a3;margin:0;line-height:1.5}
#new .order-section-icon{width:35px;height:35px;flex:none;border-radius:11px;background:#edf5ff;color:#246db3;display:grid;place-items:center;font-size:18px}
#new .order-field{min-width:0}
#new .order-field label{display:block;font-size:12px;font-weight:700;color:#344a63;margin:0 0 6px}
#new .order-field input,#new .order-field select,#new .order-field textarea{width:100%;min-width:0;box-sizing:border-box;min-height:43px;padding:9px 11px;border:1px solid #d8e2ee;border-radius:10px;background:#fbfdff;color:#1d2d42;font:13px Tahoma,Arial,sans-serif}
#new .order-field textarea{min-height:65px;resize:vertical}
#new .order-field small{display:block;font-size:10px;color:#8493a5;margin-top:5px}
#new .customer-fields{display:grid;grid-template-columns:1fr 1fr;gap:12px}
#new .contact-import-btn{display:inline-flex;align-items:center;gap:6px;margin-top:7px;border:1px solid #cbdff6;border-radius:9px;background:#edf5ff;color:#185b9c;padding:7px 10px;font:700 11px Tahoma,Arial,sans-serif}
#new .contact-import-btn .ui-icon{width:15px;height:15px}
#new .currency-field{width:170px;max-width:100%;margin-top:12px}
#new .currency-select{font-weight:700}
#new .order-items-wrap{overflow-x:auto;margin:0 -3px;padding:0 2px}
#new .itemline{grid-template-columns:minmax(112px,1.7fr) 42px 70px 70px 72px 27px!important;min-width:405px!important;gap:5px!important}
#new .itemline-head{font-size:10px;color:#647b95;font-weight:800;align-items:end}
#new .itemline input{min-height:38px!important;border-radius:8px!important;background:#fbfdff!important;font-size:11px!important;padding:6px 4px!important}
#new .itemline .lineTotal{min-height:38px!important;border-radius:8px!important;background:#edf5ff!important;border:1px solid #d7e7f8!important;color:#185b9c!important;font-size:10px!important}
#new .add-item-btn{display:inline-flex;align-items:center;gap:7px;margin:10px 0 0;border:1px dashed #8eb8e6;border-radius:10px;background:#f2f8ff;color:#1766aa;padding:9px 12px;font:700 12px Tahoma,Arial,sans-serif}
#new .add-item-btn .ui-icon{width:16px;height:16px}
#new .shipping-fields,#new .payment-fields{display:grid;grid-template-columns:1fr 1fr;gap:11px}
#new .shipping-fields input,#new .payment-fields input,#new .payment-fields select{min-height:40px!important;height:40px;padding:7px 9px}
#new #receivedAmountWrap{display:block!important;width:auto!important;max-width:none!important;min-width:0!important;flex:none!important}
#new #paymentStatus[data-state=pending]{border-color:#e7a6a1;background:#fff5f4;color:#b42318}
#new #paymentStatus[data-state=partial]{border-color:#f0cb83;background:#fff9ed;color:#9a5b08}
#new #paymentStatus[data-state=paid]{border-color:#a7d9bb;background:#f1fbf5;color:#167547}
#new .notes-section{padding:13px 15px}
#new .summary-section{background:#fffaf0;border-color:#f1e2bd}
#new .summary-section .order-section-icon{background:#fff1d6;color:#a56b12}
#new #orderSummary{margin:0!important;border:0!important;border-radius:11px!important;background:#fff5dc!important;padding:10px!important}
#new .sum-grid{display:grid!important;grid-template-columns:1fr 1fr!important;gap:8px!important}
#new .sum-item{padding:9px!important;border-radius:10px!important;background:#fff!important;border:1px solid #eee4d0!important}
#new .sum-item small{font-size:10px!important;color:#788697!important}
#new .sum-item b{font-size:14px!important;font-weight:800!important;direction:ltr!important;text-align:left!important}
#new .sum-cost b{color:#475569!important}#new .sum-sale b{color:#1769aa!important}
#new .sum-due{background:#fff3df!important;border-color:#f1d8ae!important}
#new .sum-due b{color:#a75c0a!important}#new .sum-profit{background:#effaf3!important;border-color:#ccebd8!important}
#new .sum-profit b{color:#16834b!important}
#new .order-form-actions{display:grid;grid-template-columns:1.4fr 1fr;gap:9px;margin:5px 0 0}
#new .order-form-actions button{margin:0!important;min-height:48px;border-radius:12px;font-size:13px;font-weight:800}
#new #reviewOrder{background:linear-gradient(110deg,#1769b5,#14558f)!important;box-shadow:0 4px 10px rgba(23,105,181,.18)}
#new #clearForm{background:#fff!important;border:1px solid #d6e0eb!important;color:#52657a!important}
#new input[type=number]{direction:ltr!important;text-align:left!important;font-variant-numeric:tabular-nums}
@media(max-width:430px){
 #new .order-page-shell{padding:9px 0 20px}
 #new .order-card{padding:12px;border-radius:15px;margin-bottom:11px}
 #new .customer-fields,#new .shipping-fields,#new .payment-fields{gap:8px}
 #new .order-field label{font-size:11px}
 #new .order-field input,#new .order-field select{font-size:12px}
 #new .currency-field{width:150px}
 #new .sum-item{padding:8px!important}
 #new .sum-item b{font-size:12px!important}
 #new .order-form-actions{grid-template-columns:1.25fr 1fr}
}
"""
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
