from pathlib import Path
import re

app = next(Path("appsrc").rglob("package.json")).parent
hp = app / "www" / "index.html"
jp = app / "www" / "app.js"
h = hp.read_text(encoding="utf-8")
s = jp.read_text(encoding="utf-8")

# Compact currency selector; keep the three currency choices and flags.
h = h.replace(
    '<div class="row"><div><label>العملة</label><select id="currency">',
    '<div class="row currency-row"><div><label>العملة</label><select id="currency" class="currency-select">'
)
h = h.replace(
    '<option value="SAR">🇸🇦 ريال سعودي (SAR)</option><option value="USD">🇺🇸 دولار أمريكي (USD)</option><option value="YER">🇾🇪 ريال يمني (YER)</option>',
    '<option value="SAR">🇸🇦 SAR</option><option value="USD">🇺🇸 USD</option><option value="YER">🇾🇪 YER</option>'
)
h = h.replace(
    '<span>تكلفة الوحدة</span><span>سعر بيع الوحدة</span>',
    '<span>سعر التكلفة</span><span>سعر البيع</span>'
)
h = h.replace(
    '<div><label>تكلفة الشحن الفعلية</label><input id="shippingCost" type="number" min="0" step="0.01" value="0"></div><div><label>تكلفة الشحن على العميل</label><input id="shippingCharge" type="number" min="0" step="0.01" value="0"></div>',
    '<div><label>تكلفة الشحن الفعلية</label><small class="field-hint">المبلغ الذي دفعته</small><input id="shippingCost" type="number" min="0" step="0.01" value="0"></div><div><label>تكلفة الشحن على العميل</label><small class="field-hint">المبلغ الذي يتحمله العميل</small><input id="shippingCharge" type="number" min="0" step="0.01" value="0"></div>'
)
h = h.replace('📇 دليل الهاتف', '<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 7h6M9 11h6M9 15h3"/></svg> دليل الهاتف')
h = h.replace('💾 حفظ الطلب', '<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h12l4 4v14H3V3z"/><path d="M7 3v6h10V3M7 21v-8h10v8"/></svg> حفظ الطلب')
h = h.replace('↩ إلغاء الطلب', '<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 14 4 9l5-5"/><path d="M4 9h9a7 7 0 0 1 0 14h-2"/></svg> إلغاء الطلب')
h = h.replace('＋ إضافة صنف', '<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg> إضافة صنف')
h = h.replace('<h2>💾 حفظ الطلب</h2>', '<h2>تأكيد حفظ الطلب</h2>')

style = """
.currency-row{grid-template-columns:1fr!important}
.currency-select{width:104px!important;max-width:104px!important;padding:9px 7px!important;font-size:12px!important}
.field-hint{display:block;color:#718096;font-size:10px;line-height:1.4;margin-top:-3px;margin-bottom:4px}
.itemline{grid-template-columns:minmax(112px,2fr) 36px 66px 66px 72px 26px!important;min-width:390px!important;gap:4px!important}
.itemline-head{grid-template-columns:minmax(112px,2fr) 36px 66px 66px 72px 26px!important;align-items:end}
.itemline .iqty{width:100%;padding-inline:2px!important}
.itemline input[type=number]{direction:ltr!important;text-align:left!important;font-variant-numeric:tabular-nums}
.lineTotal{display:flex;align-items:center;justify-content:flex-start;min-height:36px;padding:0 6px;border:1px solid #d4dde7;border-radius:9px;background:#f1f4f7;color:#475569;font-size:11px;font-weight:700;direction:ltr;text-align:left;white-space:nowrap;overflow:hidden}
input[type=number]{direction:ltr!important;text-align:left!important;font-variant-numeric:tabular-nums}
.ui-icon{width:18px;height:18px;display:inline-block;vertical-align:middle;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex:none}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:7px}
.action-icon{width:18px;height:18px;display:block;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.btn.icon-button{min-width:38px;min-height:38px;padding:8px;border-radius:10px}
.actions{align-items:center}
"""
h = h.replace('</style></head>', style + '</style></head>')

# Add a small, consistent outline icon set and replace item-row renderer.
icon_js = """
function uiIcon(name){
 const paths={
  edit:'<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4Z"/>',
  trash:'<path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="m19 6-1 14H6L5 6"/><path d="M10 11v5M14 11v5"/>',
  printer:'<path d="M6 9V3h12v6"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 14h12v7H6z"/><path d="M18 12h.01"/>',
  message:'<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 9 9 0 0 1-4-.9L3 21l1.7-4.5A8.4 8.4 0 1 1 21 11.5Z"/>',
  save:'<path d="M5 3h12l4 4v14H3V3z"/><path d="M7 3v6h10V3M7 21v-8h10v8"/>',
  cancel:'<circle cx="12" cy="12" r="9"/><path d="m9 9 6 6m0-6-6 6"/>',
  contact:'<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 7h6M9 11h6M9 15h3"/>',
  plus:'<path d="M12 5v14M5 12h14"/>'
 };
 return '<svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true">'+(paths[name]||'')+'</svg>';
}
"""
if 'function uiIcon(name)' not in s:
    s = s.replace('function addItemRow(item=', icon_js + '\nfunction addItemRow(item=', 1)

new_add = """function addItemRow(item={name:'',qty:'',cost:'',price:''}){
 let d=document.createElement('div');d.className='itemline';
 d.innerHTML='<input class="iname" placeholder="اسم الصنف" value="'+esc(item.name)+'"><input class="iqty" type="number" min="1" step="1" lang="en" placeholder="—" value="'+(item.qty??'')+'"><input class="icost" type="number" min="0" step=".01" lang="en" placeholder="—" value="'+(item.cost??'')+'"><input class="iprice" type="number" min="0" step=".01" lang="en" placeholder="—" value="'+(item.price??'')+'"><span class="lineTotal" role="textbox" aria-readonly="true" title="يُحسب تلقائياً ولا يمكن تعديله">0.00</span><button class="btn red delItem icon-button" type="button" aria-label="حذف الصنف" title="حذف الصنف">'+uiIcon('trash')+'</button>';
 $('items').append(d);d.querySelectorAll('input').forEach(x=>{x.lang='en';x.addEventListener('input',()=>{updateLineTotal(d);calcSummary();syncFullPayment();});});
 d.querySelector('.delItem').onclick=()=>{d.remove();calcSummary();syncFullPayment();};updateLineTotal(d);calcSummary();
}"""
s,n = re.subn(r'function addItemRow\(item=.*?\n\}', new_add, s, count=1, flags=re.S)
if n != 1: raise SystemExit('Could not replace addItemRow safely')

new_card = """function orderCard(o){
 const t=totals(o),st=paymentState(o);
 return '<div class="panel order-card"><div class="row"><div><b>'+esc(o.customerName)+'</b><div class="muted">'+esc(o.id)+' · '+esc(o.date||'')+'</div><div class="muted">'+esc(o.customerPhone||'')+'</div></div><div><b>'+money(t.due,o.currency)+'</b><div class="pill">'+esc(st)+'</div><div class="muted">المتبقي: '+money(Math.max(0,t.due-Number(o.amountReceived||0)),o.currency)+'</div></div></div><div class="actions"><button class="btn light icon-button" data-action="edit" data-id="'+esc(o.id)+'" aria-label="تعديل" title="تعديل">'+uiIcon('edit')+'</button><button class="btn red icon-button" data-action="delete" data-id="'+esc(o.id)+'" aria-label="حذف" title="حذف">'+uiIcon('trash')+'</button><button class="btn light icon-button" data-action="print" data-id="'+esc(o.id)+'" aria-label="طباعة الفاتورة" title="طباعة الفاتورة">'+uiIcon('printer')+'</button><button class="btn whatsapp icon-button" data-action="whatsapp" data-id="'+esc(o.id)+'" aria-label="واتساب" title="واتساب">'+uiIcon('message')+'</button></div></div>';
}"""
s,n = re.subn(r'function orderCard\(o\)\{.*?\n\}', new_card, s, count=1, flags=re.S)
if n != 1: raise SystemExit('Could not replace orderCard safely')

# Make the phonebook, save, cancel and add-item controls use the same outline icon family.
s = s.replace("alert('ميزة دليل الهاتف غير متاحة في هذه النسخة')", "alert('ميزة دليل الهاتف غير متاحة في هذه النسخة')")
s = s.replace("printInvoice(id);", "printInvoice(id);")
# Update stale validation wording to match the approved labels.
s = s.replace('سعر بيع الوحدة لا يمكن أن يكون أقل من تكلفة الوحدة', 'سعر البيع لا يمكن أن يكون أقل من سعر التكلفة')
hp.write_text(h, encoding="utf-8")
jp.write_text(s, encoding="utf-8")
print("Approved UI changes applied")
