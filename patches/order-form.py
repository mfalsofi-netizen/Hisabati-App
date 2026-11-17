from pathlib import Path

app = next(Path("appsrc").rglob("package.json")).parent
html = app / "www" / "index.html"
js = app / "www" / "app.js"
h = html.read_text(encoding="utf-8")
s = js.read_text(encoding="utf-8")

# Compact numeric columns; keep the item name as the widest column.
h = h.replace(
    ".itemline{display:grid;grid-template-columns:minmax(150px,2fr) 70px 110px 110px 40px;gap:6px;min-width:560px;margin:7px 0}.itemline input{min-width:0}",
    ".itemline{display:grid;grid-template-columns:minmax(118px,2fr) 48px 76px 76px 32px;gap:4px;min-width:370px;margin:7px 0;align-items:center}.itemline input{min-width:0;width:100%;padding:8px 3px;font-size:12px;text-align:center}.itemline .iname{text-align:right;padding-inline:8px;font-size:13px}.itemline-head{font-size:11px;line-height:1.35}.itemline .delItem{padding:5px 0!important;margin:0!important}"
)
h = h.replace(
    '<div class="row"><div><label>اسم العميل</label><input id="customerName" placeholder="اسم العميل"></div><div><label>رقم الهاتف</label><input id="customerPhone" inputmode="tel" placeholder="رقم الهاتف"></div></div>',
    '<div class="row"><div><label>اسم العميل</label><input id="customerName" placeholder="اسم العميل"></div><div><label>رقم الهاتف</label><input id="customerPhone" inputmode="tel" placeholder="رقم الهاتف"><button type="button" class="btn light" id="pickContact">استيراد من دليل الهاتف</button></div></div>'
)
h = h.replace(
    '<div class="row"><div><label>العملة</label><select id="currency"><option value="SAR">ريال سعودي (SAR)</option><option value="USD">دولار أمريكي (USD)</option></select></div><div><label>حالة الطلب</label><select id="status"><option>بانتظار الدفع</option><option>تم استلام المبلغ</option><option>تم الشراء</option><option>تم الشحن</option><option>مكتمل</option></select></div></div>',
    '<div class="row"><div><label>العملة</label><select id="currency"><option value="SAR">ريال سعودي (SAR)</option><option value="USD">دولار أمريكي (USD)</option></select></div><div><label>حالة تنفيذ الطلب</label><select id="status"><option>جديد</option><option>تم الشراء</option><option>تم الشحن</option><option>مكتمل</option></select></div></div><div class="row"><div><label>حالة الدفع</label><select id="paymentStatus" class="payment-status"><option value="بانتظار الدفع">بانتظار الدفع</option><option value="تم استلام جزء من المبلغ">تم استلام جزء من المبلغ</option><option value="تم استلام المبلغ بالكامل">تم استلام المبلغ بالكامل</option></select></div><div id="receivedAmountWrap" class="hidden"><label>المبلغ المستلم</label><input id="amountReceived" type="number" min="0" step=".01" value="0"></div></div>'
)
h = h.replace(
    '<div class="itemline" style="font-weight:bold"><span>الصنف</span><span>الكمية</span><span>تكلفة الوحدة</span><span>سعر بيع الوحدة</span><span></span></div>',
    '<div class="itemline itemline-head"><span>الصنف</span><span>الكمية</span><span>تكلفة الوحدة</span><span>سعر بيع الوحدة</span><span></span></div>'
)
h = h.replace(
    ".pill{display:inline-block;background:#eaf5ff;color:#17558d;border-radius:20px;padding:4px 8px;font-size:11px}",
    ".pill{display:inline-block;background:#eaf5ff;color:#17558d;border-radius:20px;padding:4px 8px;font-size:11px}.payment-status{font-weight:bold}.payment-status[data-state='pending']{color:#b42318;border-color:#b42318;background:#fff1f0}.payment-status[data-state='partial']{color:#a15c00;border-color:#d97706;background:#fff7e6}.payment-status[data-state='paid']{color:#16834b;border-color:#16834b;background:#edfff4}.payment-pill.pending{background:#fff1f0;color:#b42318}.payment-pill.partial{background:#fff7e6;color:#a15c00}.payment-pill.paid{background:#edfff4;color:#16834b}"
)
html.write_text(h, encoding="utf-8")

s = s.replace(
    "function addItemRow(item={name:'',qty:1,cost:0,price:0}){",
    "function addItemRow(item={name:'',qty:1,cost:0,price:0}){"
)
s = s.replace(
    "return {id:$('editId').value||('ORD-'+Date.now()),date:today(),customerName:$('customerName').value.trim(),customerPhone:$('customerPhone').value.trim(),currency:$('currency').value,status:$('status').value,items,shippingCost:Number($('shippingCost').value||0),shippingCharge:Number($('shippingCharge').value||0),notes:$('orderNotes').value};",
    "return {id:$('editId').value||('ORD-'+Date.now()),date:today(),customerName:$('customerName').value.trim(),customerPhone:$('customerPhone').value.trim(),currency:$('currency').value,status:$('status').value,paymentStatus:$('paymentStatus').value,amountReceived:Number($('amountReceived').value||0),items,shippingCost:Number($('shippingCost').value||0),shippingCharge:Number($('shippingCharge').value||0),notes:$('orderNotes').value};"
)
s = s.replace(
    "if(o.shippingCost<0||o.shippingCharge<0)return 'قيمة الشحن لا يمكن أن تكون سالبة';return '';",
    "if(o.shippingCost<0||o.shippingCharge<0)return 'قيمة الشحن لا يمكن أن تكون سالبة';let due=totals(o).due;if(o.paymentStatus==='بانتظار الدفع'&&o.amountReceived!==0)return 'اجعل المبلغ المستلم صفراً أو غيّر حالة الدفع';if(o.paymentStatus==='تم استلام جزء من المبلغ'&&!(o.amountReceived>0&&o.amountReceived<due))return 'المبلغ المستلم جزئياً يجب أن يكون أكبر من صفر وأقل من إجمالي المستحق';if(o.paymentStatus==='تم استلام المبلغ بالكامل'&&Math.abs(o.amountReceived-due)>0.001)return 'عند اختيار استلام المبلغ بالكامل يجب أن يساوي المبلغ المستلم إجمالي المستحق';return '';"
)
s = s.replace(
    "$('reviewBody').innerHTML=`<p>العميل: <b>${esc(o.customerName)}</b> — ${esc(o.customerPhone)}</p><p>العملة: ${o.currency} — الحالة: ${esc(o.status)}</p>",
    "$('reviewBody').innerHTML=`<p>العميل: <b>${esc(o.customerName)}</b> — ${esc(o.customerPhone)}</p><p>العملة: ${o.currency} — تنفيذ الطلب: ${esc(o.status)} — حالة الدفع: ${esc(o.paymentStatus)}</p><p>المبلغ المستلم: <b>${money(o.amountReceived,o.currency)}</b> — المتبقي: <b>${money(Math.max(0,t.due-o.amountReceived),o.currency)}</b></p>"
)
s = s.replace(
    "function clearForm(){$('editId').value='';$('formTitle').textContent='طلب جديد';['customerName','customerPhone','orderNotes'].forEach(x=>$(x).value='');$('currency').value='SAR';$('status').value='بانتظار الدفع';$('shippingCost').value=0;",
    "function clearForm(){$('editId').value='';$('formTitle').textContent='طلب جديد';['customerName','customerPhone','orderNotes'].forEach(x=>$(x).value='');$('currency').value='SAR';$('status').value='جديد';$('paymentStatus').value='بانتظار الدفع';$('amountReceived').value=0;updatePaymentFields();$('shippingCost').value=0;"
)
s = s.replace(
    "$('status').value=o.status;$('shippingCost').value=o.shippingCost;",
    "$('status').value=o.status||'جديد';$('paymentStatus').value=o.paymentStatus||(o.status==='تم استلام المبلغ'?'تم استلام المبلغ بالكامل':'بانتظار الدفع');$('amountReceived').value=o.amountReceived??(o.paymentStatus==='تم استلام المبلغ بالكامل'?totals(o).due:0);updatePaymentFields();$('shippingCost').value=o.shippingCost;"
)
s = s.replace(
    "function orderCard(o){let t=totals(o);return `<div class=\"panel\"><div class=\"row\"><div><b>${esc(o.customerName)}</b><div class=\"muted\">${esc(o.id)} · ${o.date} · ${esc(o.customerPhone)}</div></div><div><span class=\"pill\">${esc(o.status)}</span><div><b>${money(t.due,o.currency)}</b></div></div></div><div class=\"muted\">صافي الربح: ${money(t.profit,o.currency)}</div>",
    "function orderCard(o){let t=totals(o),ps=o.paymentStatus||(o.status==='تم استلام المبلغ'?'تم استلام المبلغ بالكامل':'بانتظار الدفع'),pc=ps==='بانتظار الدفع'?'pending':ps==='تم استلام جزء من المبلغ'?'partial':'paid';return `<div class=\"panel\"><div class=\"row\"><div><b>${esc(o.customerName)}</b><div class=\"muted\">${esc(o.id)} · ${o.date} · ${esc(o.customerPhone)}</div></div><div><span class=\"pill\">${esc(o.status||'جديد')}</span> <span class=\"pill payment-pill ${pc}\">${esc(ps)}</span><div><b>${money(t.due,o.currency)}</b></div><div class=\"muted\">المتبقي: ${money(Math.max(0,t.due-(o.amountReceived||0)),o.currency)}</div></div></div><div class=\"muted\">صافي الربح: ${money(t.profit,o.currency)}</div>"
)
s = s.replace(
    "function renderOrders(){let q=($('orderSearch')?.value||'').toLowerCase(),st=$('filterStatus')?.value||'',cu=$('filterCurrency')?.value||'';let arr=orders.filter(o=>(!q||[o.id,o.customerName,o.customerPhone].join(' ').toLowerCase().includes(q))&&(!st||o.status===st)&&(!cu||o.currency===cu));",
    "function renderOrders(){let q=($('orderSearch')?.value||'').toLowerCase(),st=$('filterStatus')?.value||'',cu=$('filterCurrency')?.value||'';let arr=orders.filter(o=>(!q||[o.id,o.customerName,o.customerPhone].join(' ').toLowerCase().includes(q))&&(!st||(o.paymentStatus||(o.status==='تم استلام المبلغ'?'تم استلام المبلغ بالكامل':'بانتظار الدفع'))===st)&&(!cu||o.currency===cu));"
)
s = s.replace(
    "a.filter(x=>x.status==='بانتظار الدفع').length",
    "a.filter(x=>(x.paymentStatus||'بانتظار الدفع')==='بانتظار الدفع').length"
).replace(
    "a.filter(x=>x.status!=='بانتظار الدفع').length",
    "a.filter(x=>(x.paymentStatus||'بانتظار الدفع')!=='بانتظار الدفع').length"
)
s = s.replace(
    "let overdue=orders.filter(o=>o.status==='بانتظار الدفع'&&",
    "let overdue=orders.filter(o=>(o.paymentStatus||'بانتظار الدفع')==='بانتظار الدفع'&&"
)

# Update the payment selector visual state and partial-payment amount visibility.
payment_logic = """
function updatePaymentFields(){
  const state=$('paymentStatus').value,wrap=$('receivedAmountWrap'),sel=$('paymentStatus');
  wrap.classList.toggle('hidden',state!=='تم استلام جزء من المبلغ');
  sel.dataset.state=state==='بانتظار الدفع'?'pending':state==='تم استلام جزء من المبلغ'?'partial':'paid';
  if(state==='بانتظار الدفع')$('amountReceived').value=0;
  if(state==='تم استلام المبلغ بالكامل'){
    const o={items:getItems(),shippingCharge:$('shippingCharge').value,currency:$('currency').value};
    $('amountReceived').value=totals(o).due;
  }
}
$('paymentStatus').addEventListener('change',updatePaymentFields);
$('amountReceived').addEventListener('input',()=>{});
$('shippingCharge').addEventListener('input',()=>{if($('paymentStatus').value==='تم استلام المبلغ بالكامل')updatePaymentFields();});
$('currency').addEventListener('change',()=>{if($('paymentStatus').value==='تم استلام المبلغ بالكامل')updatePaymentFields();});
"""
if "function updatePaymentFields()" not in s:
    s = s.replace("$('addItem').onclick=()=>addItemRow();", "$('addItem').onclick=()=>addItemRow();\n"+payment_logic)

# Native Android system contact picker. The picker returns one selected phone number.
contact_logic = """
$('pickContact').onclick=async()=>{
  try{
    const picker=window.Capacitor?.Plugins?.HisabatiContacts;
    if(!picker?.pick){alert('ميزة دليل الهاتف غير متاحة في هذه النسخة');return;}
    const result=await picker.pick();
    if(result?.name)$('customerName').value=result.name;
    if(result?.phone)$('customerPhone').value=result.phone;
  }catch(e){if(!String(e?.message||e).toLowerCase().includes('cancel'))alert('تعذر اختيار جهة الاتصال: '+(e?.message||e));}
};
"""
if "$('pickContact').onclick" not in s:
    s = s.replace("$('nav').addEventListener('click'", contact_logic+"\n$('nav').addEventListener('click'")

# Keep filters aligned with payment status.
h = html.read_text(encoding="utf-8")
h = h.replace(
    '<select id="filterStatus"><option value="">كل الحالات</option><option>بانتظار الدفع</option><option>تم استلام المبلغ</option><option>تم الشراء</option><option>تم الشحن</option><option>مكتمل</option></select>',
    '<select id="filterStatus"><option value="">كل حالات الدفع</option><option>بانتظار الدفع</option><option>تم استلام جزء من المبلغ</option><option>تم استلام المبلغ بالكامل</option></select>'
)
html.write_text(h, encoding="utf-8")
js.write_text(s, encoding="utf-8")
print("Applied customer picker, payment states, and compact numeric item fields")
