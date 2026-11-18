from pathlib import Path
import re

app = next(Path("appsrc").rglob("package.json")).parent
hp, jp = app/"www"/"index.html", app/"www"/"app.js"
h, s = hp.read_text(encoding="utf-8"), jp.read_text(encoding="utf-8")

section = r'''<section id="new" class="page hidden">
<div class="ref-order">
  <div class="ref-head">
    <svg viewBox="0 0 64 64" aria-hidden="true"><path d="M5 9h8l6 31a5 5 0 0 0 5 4h27a5 5 0 0 0 5-4l5-23H17" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="26" cy="54" r="5" fill="currentColor"/><circle cx="49" cy="54" r="5" fill="currentColor"/></svg>
    <h2 id="formTitle">طلب جديد</h2>
    <svg viewBox="0 0 64 64" aria-hidden="true"><path d="M8 14h48M8 32h48M8 50h48" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round"/></svg>
  </div>
  <input type="hidden" id="editId"><input type="hidden" id="orderNotes" value="">
  <input type="hidden" id="currency" value="SAR">
  <section class="ref-card ref-customer">
    <div class="ref-customer-cell">
      <label for="customerName"><svg viewBox="0 0 32 32"><circle cx="16" cy="9" r="7" fill="currentColor"/><path d="M3 29c0-8 5-12 13-12s13 4 13 12" fill="currentColor"/></svg>اسم العميل</label>
      <input id="customerName" placeholder="اسم العميل" autocomplete="off">
    </div>
    <div class="ref-customer-cell">
      <label for="customerPhone"><svg viewBox="0 0 32 32"><path d="M7 3 3 7c0 12 10 22 22 22l4-4-7-6-4 3c-4-2-7-5-9-9l3-4z" fill="currentColor"/></svg>رقم الموبايل</label>
      <input id="customerPhone" inputmode="tel" placeholder="رقم الموبايل" autocomplete="off">
      <button type="button" id="pickContact" class="ref-contact-pick" aria-label="اختيار من دليل الهاتف"></button>
    </div>
  </section>
  <section class="ref-card ref-items">
    <div class="ref-section-head">
      <span><svg viewBox="0 0 44 44"><path d="m22 2 19 10v20L22 42 3 32V12z" fill="currentColor"/><path d="m3 12 19 10 19-10M22 22v20" fill="none" stroke="#fff" stroke-width="2"/></svg>الأصناف</span>
      <button type="button" id="addItem"><b>＋</b> إضافة صنف</button>
    </div>
    <div class="ref-table-scroll">
      <div class="ref-table-head"><span>الصنف</span><span>الكمية</span><span>سعر التكلفة</span><span>سعر البيع</span><span>الإجمالي</span><i></i></div>
      <div id="items"></div>
    </div>
  </section>
  <section class="ref-card ref-shipping">
    <div class="ref-section-head"><span><svg viewBox="0 0 48 42"><path d="M2 5h28v25H2zM30 14h9l7 9v7H30z" fill="currentColor"/><circle cx="12" cy="33" r="6" fill="currentColor"/><circle cx="38" cy="33" r="6" fill="currentColor"/><circle cx="12" cy="33" r="2" fill="#fff"/><circle cx="38" cy="33" r="2" fill="#fff"/></svg>تكاليف الشحن</span></div>
    <div class="ref-shipping-grid">
      <div class="ref-field"><label for="shippingCharge">تكلفة الشحن على العميل</label><input id="shippingCharge" type="number" min="0" step=".01" value="0"></div>
      <div class="ref-field"><label for="shippingCost">تكلفة الشحن الفعلية</label><input id="shippingCost" type="number" min="0" step=".01" value="0"></div>
    </div>
  </section>
  <section class="ref-card ref-received">
    <label for="amountReceived"><svg viewBox="0 0 40 44"><path d="M13 4h14l-2 7h-10zM9 12h22l5 23c1 4-2 6-6 6H10c-4 0-7-2-6-6z" fill="currentColor"/><path d="M20 18v16m6-12c-2-3-10-3-11 1-1 4 11 3 11 7s-9 5-13 1" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/></svg>المبلغ المستلم</label>
    <input id="amountReceived" type="number" min="0" step=".01" value="0" inputmode="decimal">
  </section>
  <section class="ref-card ref-summary">
    <div class="ref-summary-head"><span><svg viewBox="0 0 36 36"><rect x="5" y="2" width="26" height="32" rx="3" fill="currentColor"/><path d="M11 8h14M11 16h4m6 0h4m-14 6h4m6 0h4m-14 6h4m6 0h4" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/></svg>ملخص الطلب</span></div>
    <div id="orderSummary" class="ref-summary-grid"></div>
  </section>
  <div class="ref-actions">
    <button type="button" id="clearForm" class="ref-reset"><svg viewBox="0 0 40 40"><path d="M7 15A14 14 0 1 1 5 24M7 5v10h10" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>إعادة تعيين</button>
    <button type="button" id="reviewOrder" class="ref-save"><svg viewBox="0 0 40 40"><path d="M5 3h25l7 7v27H3V3z" fill="currentColor"/><path d="M10 3v12h19V3M10 37V22h20v15" fill="none" stroke="#fff" stroke-width="3"/><rect x="14" y="25" width="12" height="12" fill="#fff"/></svg>حفظ الطلب</button>
  </div>
</div>
</section>'''
h, n = re.subn(r'<section id="new" class="page hidden">.*?(?=<section id="customers")', section+"\n", h, count=1, flags=re.S)
if n != 1: raise SystemExit("New-order section not found; refusing unsafe patch")

css = r"""
/* Screenshot-led recreation of the approved 1024x1536 New Order screen */
#new{padding:0!important;background:#f6f9ff!important}
#new .ref-order{width:100%;max-width:520px;margin:0 auto;padding:0 12px 18px;direction:rtl;color:#202b3e;font-family:Tahoma,Arial,sans-serif}
#new .ref-head{height:58px;margin:0 -12px 10px;padding:0 17px;display:grid;grid-template-columns:44px 1fr 44px;align-items:center;background:linear-gradient(110deg,#1268bd,#07519d);border-radius:0 0 17px 17px;color:#fff}
#new .ref-head h2{margin:0!important;text-align:center;color:#fff!important;font-size:25px!important;font-weight:800!important}
#new .ref-head svg{width:34px;height:34px;fill:currentColor}
#new .ref-card{background:#fff;border:1px solid #c8daf2;border-radius:15px;margin:0 0 10px;box-shadow:0 2px 7px rgba(18,83,157,.07);overflow:hidden}
#new .ref-customer{display:grid;grid-template-columns:1fr 1fr;padding:10px;min-height:86px}
#new .ref-customer-cell{min-width:0;position:relative;padding:0 9px}
#new .ref-customer-cell+ .ref-customer-cell{border-right:1px solid #a9c4e8}
#new .ref-customer-cell label{height:24px;display:flex;align-items:center;gap:7px;margin:0 0 5px;font-size:15px;font-weight:800;color:#153a69}
#new .ref-customer-cell label svg{width:21px;height:21px;color:#1268c9;flex:none}
#new .ref-customer-cell input{height:39px;width:100%;min-width:0;padding:5px 10px;border:1px solid #cbd4e2;border-radius:10px;background:#fcfcfd;font:16px Tahoma,Arial,sans-serif;color:#252b39;text-align:right}
#new .ref-contact-pick{position:absolute;inset-inline-start:8px;top:0;width:22px;height:23px;opacity:0;z-index:2}
#new .ref-section-head{height:43px;padding:0 11px;display:flex;align-items:center;justify-content:space-between;background:linear-gradient(100deg,#dcecff,#c8e0ff);color:#104f95;font-size:20px;font-weight:800}
#new .ref-section-head>span{display:flex;align-items:center;gap:8px}
#new .ref-section-head svg{width:29px;height:29px;flex:none}
#new .ref-section-head button{height:34px;border:0;border-radius:10px;padding:0 12px;background:linear-gradient(110deg,#1878d3,#0758a8);color:#fff;font:700 16px Tahoma;white-space:nowrap}
#new .ref-section-head button b{font-size:24px;vertical-align:-2px;margin-inline-start:5px}
#new .ref-table-scroll{padding:4px 6px 7px;overflow-x:auto}
#new .ref-table-head,#new .ref-item-row{display:grid;grid-template-columns:minmax(94px,1.65fr) 48px 76px 76px 76px 32px;gap:5px;align-items:center;min-width:420px;text-align:center}
#new .ref-table-head{height:31px;border-radius:7px;background:#edf5ff;color:#173a68;font-size:11px;font-weight:800}
#new .ref-item-row{min-height:43px;padding:4px 0;border-bottom:1px solid #e0e8f4}
#new .ref-item-row input{width:100%;height:36px;min-width:0;padding:3px;border:1px solid #e0e7f0;border-radius:8px;background:#fff;box-shadow:0 2px 5px #102c520d;font:13px Tahoma;color:#202638;text-align:center}
#new .ref-item-row .iname{text-align:right;padding-inline:8px;font-size:13px}
#new .ref-item-row .iqty{font-size:13px;font-weight:700}
#new .ref-item-row .lineTotal{height:36px;display:flex;align-items:center;justify-content:center;border-radius:8px;background:#e2efff;color:#075cc2;font-size:13px;font-weight:800;direction:ltr;white-space:nowrap}
#new .ref-item-row .delItem{width:32px;height:32px;padding:0!important;margin:0!important;border:0;border-radius:50%;background:#ed2937;color:white;font-size:0;display:grid;place-items:center}
#new .ref-item-row .delItem svg{width:19px;height:19px}
#new .ref-shipping .ref-section-head{height:42px}
#new .ref-shipping-grid{display:grid;grid-template-columns:1fr 1fr;padding:7px 9px 9px;gap:12px}
#new .ref-field{min-width:0;padding:0 8px}
#new .ref-field+ .ref-field{border-right:1px solid #b5c9e5}
#new .ref-field label{display:block;text-align:center;margin:0 0 5px;font-size:14px;font-weight:700;color:#344057}
#new .ref-field input{height:38px;width:100%;padding:5px 8px;border:1px solid #cbd5e3;border-radius:9px;background:#fcfcfd;font:17px Tahoma;text-align:center!important;direction:ltr;font-variant-numeric:tabular-nums}
#new .ref-received{display:grid;grid-template-columns:1fr 1fr;align-items:center;min-height:53px;padding:8px 12px}
#new .ref-received label{display:flex;align-items:center;gap:8px;margin:0;font-size:17px;font-weight:800;color:#39435a}
#new .ref-received label svg{width:31px;height:34px;color:#0872c9}
#new .ref-received input{height:39px;width:100%;padding:5px 10px;border:1px solid #b7d2f4;border-radius:10px;background:#e9f3ff;font:18px Tahoma;font-weight:700;text-align:center;direction:ltr;font-variant-numeric:tabular-nums}
#new .ref-summary{border-color:#c5dafa}
#new .ref-summary-head{height:43px;background:linear-gradient(110deg,#1265b5,#07519d);color:#fff;padding:0 12px;display:flex;align-items:center;justify-content:flex-start}
#new .ref-summary-head span{display:flex;align-items:center;gap:8px;font-size:19px;font-weight:800}
#new .ref-summary-head svg{width:27px;height:27px}
#new .ref-summary-grid{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;padding:8px 5px;min-height:80px}
#new .ref-summary-item{min-width:0;padding:3px 4px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;border-left:1px solid #b7cce9}
#new .ref-summary-item:last-child{border-left:0}
#new .ref-summary-item small{font-size:11px;line-height:1.35;color:#3e4b63;font-weight:700}
#new .ref-summary-item strong{margin-top:6px;font-size:17px;line-height:1.15;white-space:nowrap;direction:ltr;font-variant-numeric:tabular-nums}
#new .ref-summary-cost strong{color:#46516b}
#new .ref-summary-sale strong{color:#075fc6}
#new .ref-summary-shipping strong{color:#f06c00}
#new .ref-summary-due{background:#fff0d5;border-radius:9px}
#new .ref-summary-due small{color:#18283d}
#new .ref-summary-due strong{color:#a94d00;font-size:20px}
#new .ref-actions{display:grid;grid-template-columns:1fr 1.25fr;gap:9px;margin:12px 1px 0}
#new .ref-actions button{height:56px;border-radius:15px;display:flex;align-items:center;justify-content:center;gap:9px;font:800 18px Tahoma}
#new .ref-actions svg{width:29px;height:29px;flex:none}
#new .ref-reset{background:#f5f7fb;border:1px solid #9aacc8;color:#3c4964}
#new .ref-save{background:linear-gradient(110deg,#1678d5,#0755a4);border:0;color:#fff;box-shadow:0 3px 8px #0755a422}
#new .hidden{display:none!important}
@media(max-width:390px){#new .ref-order{padding-inline:8px}#new .ref-head{margin-inline:-8px}#new .ref-summary-item small{font-size:9px}#new .ref-summary-item strong{font-size:14px}#new .ref-summary-due strong{font-size:17px}#new .ref-customer-cell{padding-inline:5px}}
"""
h = h.replace("</style></head>", css+"\n</style></head>", 1)

# Preserve the native Android contacts picker while keeping the screenshot clean:
# its invisible hit target sits over the phone icon position.
# Replace item editor with the six-column layout matching the reference.
s = re.sub(r"function addItemRow\(.*?(?=\nfunction getItems\(\))", r'''function addItemRow(item={name:'',qty:'',cost:'',price:''}){
 const d=document.createElement('div');d.className='ref-item-row';
 d.innerHTML='<input class="iname" placeholder="اسم الصنف" value="'+esc(item.name)+'"><input class="iqty" type="number" min="1" step="1" lang="en-US" placeholder="—" value="'+(item.qty??'')+'"><input class="icost" type="number" min="0" step=".01" lang="en-US" placeholder="—" value="'+(item.cost??'')+'"><input class="iprice" type="number" min="0" step=".01" lang="en-US" placeholder="—" value="'+(item.price??'')+'"><span class="lineTotal">0.00</span><button type="button" class="delItem" aria-label="حذف الصنف"><svg viewBox="0 0 24 24"><path d="M4 7h16M9 7V4h6v3m-9 0 1 14h10l1-14M10 11v6m4-6v6" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>';
 $('items').append(d);
 d.querySelectorAll('input').forEach(x=>x.addEventListener('input',()=>{updateLineTotal(d);calcSummary();}));
 d.querySelector('.delItem').onclick=()=>{d.remove();calcSummary();};
 updateLineTotal(d);calcSummary();
}
function updateLineTotal(r){const q=Number(r.querySelector('.iqty').value||0),p=Number(r.querySelector('.iprice').value||0);r.querySelector('.lineTotal').textContent=(q*p).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
''',s,count=1,flags=re.S)
s = re.sub(r"function calcSummary\(\)\{.*?(?=\n\$\(?'addItem'\)?\.onclick)", r'''function calcSummary(){
 const o={items:getItems(),shippingCost:$('shippingCost').value,shippingCharge:$('shippingCharge').value,currency:$('currency').value},t=totals(o);
 $('orderSummary').innerHTML='<div class="ref-summary-item ref-summary-cost"><small>إجمالي تكلفة البضاعة</small><strong>'+money(t.cost,o.currency)+'</strong></div><div class="ref-summary-item ref-summary-sale"><small>إجمالي بيع البضاعة</small><strong>'+money(t.sale,o.currency)+'</strong></div><div class="ref-summary-item ref-summary-shipping"><small>الشحن على العميل</small><strong>'+money(t.sh,o.currency)+'</strong></div><div class="ref-summary-item ref-summary-due"><small>المطلوب من العميل</small><strong>'+money(t.due,o.currency)+'</strong></div>';
}
''',s,count=1,flags=re.S)

# Amount received is the sole payment input. Payment state is derived for legacy
# reports/order lists, never shown as a selectable field.
s = re.sub(r"function formData\(\)\{.*?(?=\nfunction validate\(o\)\{)", r'''function formData(){
 const items=getItems(),received=Number($('amountReceived').value||0);
 const o={id:$('editId').value||('ORD-'+Date.now()),date:today(),customerName:$('customerName').value.trim(),customerPhone:$('customerPhone').value.trim(),currency:$('currency').value||'SAR',status:'جديد',items,shippingCost:Number($('shippingCost').value||0),shippingCharge:Number($('shippingCharge').value||0),amountReceived:received,notes:$('orderNotes').value};
 const due=totals(o).due;o.paymentStatus=received<=0?'بانتظار الدفع':received>=due?'تم استلام المبلغ بالكامل':'تم استلام جزء من المبلغ';
 return o;
}
''',s,count=1,flags=re.S)
s = re.sub(r"function validate\(o\)\{.*?\n\}", r'''function validate(o){
 if(!o.customerName)return 'أدخل اسم العميل';
 if(!o.items.length)return 'أضف صنفاً واحداً على الأقل';
 for(const x of o.items){if(!x.name||!(x.qty>0)||x.cost<0||x.price<0)return 'تحقق من بيانات الأصناف';if(x.price<x.cost)return 'سعر بيع الوحدة لا يمكن أن يكون أقل من تكلفة الوحدة';}
 if(o.shippingCost<0||o.shippingCharge<0)return 'قيمة الشحن لا يمكن أن تكون سالبة';
 const due=totals(o).due;
 if(!Number.isFinite(o.amountReceived)||o.amountReceived<0)return 'أدخل مبلغاً مستلماً صحيحاً';
 if(o.amountReceived>due)return 'المبلغ المستلم لا يمكن أن يتجاوز المبلغ المطلوب';
 return '';
}''',s,count=1,flags=re.S)

# Remove the old review step: the blue button saves immediately, then shows the centered receipt.
s = re.sub(r"\$\(?'reviewOrder'\)?\.onclick=.*?;\n\$\(?'backEdit'\)?\.onclick=.*?;\n", "", s, count=1, flags=re.S)
s += r'''
function showSavedOrderSummary(o){
 const t=totals(o),received=Number(o.amountReceived||0),remaining=Math.max(0,t.due-received),fmt=v=>new Intl.NumberFormat('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}).format(Number(v||0));
 document.getElementById('saveSuccessOverlay')?.remove();
 const overlay=document.createElement('div');overlay.id='saveSuccessOverlay';
 overlay.style.cssText='position:fixed;inset:0;z-index:100000;background:rgba(15,30,55,.48);display:flex;align-items:center;justify-content:center;padding:5vw;direction:rtl';
 overlay.innerHTML='<section id="saveSuccessCard" style="width:100%;max-width:470px;max-height:90vh;overflow:auto;background:#fff;border-radius:28px;padding:22px 18px;box-shadow:0 18px 55px #0004;font-family:Tahoma,Arial"><div style="display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #dce4ef;padding-bottom:14px"><span style="font-size:30px;color:#0b9d55">● ✓</span><b style="font-size:23px;color:#0b9850">تم حفظ الطلب بنجاح</b><button id="closeSavedX" style="border:0;background:none;font-size:30px;color:#748094">×</button></div><div style="padding:12px 4px;font-size:18px;line-height:1.9"><div>رقم الطلب: <b style="color:#1265bd;direction:ltr">'+esc(o.id)+'</b></div><div>اسم العميل: <b>'+esc(o.customerName)+'</b></div><div>عدد الأصناف: <b>'+o.items.length+' أصناف</b></div></div><div style="border:1px solid #c4ddfa;border-radius:14px;overflow:hidden"><div style="background:#dceeff;text-align:center;padding:10px;font-size:21px;font-weight:bold;color:#123d6b">ملخص المبالغ</div>'+[['إجمالي تكلفة البضاعة',t.cost],['إجمالي بيع البضاعة',t.sale],['الشحن الفعلي',t.sc],['الشحن على العميل',t.sh],['المطلوب من العميل',t.due],['المبلغ المستلم',received],['المبلغ المتبقي',remaining]].map((x,i)=>'<div style="display:flex;justify-content:space-between;padding:10px 12px;border-bottom:1px solid #e2eaf4;background:'+(i===4?'#fff0d4':'#fff')+';font-size:16px"><span>'+x[0]+'</span><b style="direction:ltr;color:'+(i===4?'#bd6200':i===5?'#159b57':i===6?'#d22':'#29364b')+'">'+fmt(x[1])+'</b></div>').join('')+'</div><div style="display:flex;justify-content:space-between;padding:14px 6px;font-size:18px"><span>العملة:</span><b>🇸🇦 SAR</b></div><button id="closeSavedOk" style="width:100%;padding:15px;border:0;border-radius:13px;background:#176fc4;color:white;font:bold 20px Tahoma">✓　حسناً</button></section>';
 document.body.appendChild(overlay);const close=()=>overlay.remove();overlay.querySelector('#closeSavedX').onclick=close;overlay.querySelector('#closeSavedOk').onclick=close;overlay.addEventListener('click',e=>{if(e.target===overlay)close();});
}
$('reviewOrder').onclick=async()=>{
 const o=formData(),err=validate(o);if(err){alert(err);return;}
 try{const idx=orders.findIndex(x=>x.id===o.id);if(idx>=0)orders[idx]=o;else orders.unshift(o);await saveAll();clearForm();showPage('orders');showSavedOrderSummary(o);}
 catch(e){alert('تعذر حفظ الطلب: '+(e?.message||e));}
};
'''
# Fix reset/edit logic for removed status controls and retain old saved records.
s = re.sub(r"function clearForm\(\)\s*\{.*?\n\}\s*function editOrder\(id\)\s*\{.*?\n\}", r'''function clearForm(){
 $('editId').value='';$('formTitle').textContent='طلب جديد';
 ['customerName','customerPhone','orderNotes'].forEach(id=>{if($(id))$(id).value='';});
 $('currency').value='SAR';$('amountReceived').value='0';$('shippingCost').value='0';$('shippingCharge').value='0';$('items').innerHTML='';addItemRow();calcSummary();
}
function editOrder(id){
 const o=orders.find(x=>x.id===id);if(!o)return;showPage('new');$('editId').value=o.id;$('formTitle').textContent='تعديل الطلب';
 $('customerName').value=o.customerName||'';$('customerPhone').value=o.customerPhone||'';$('currency').value=o.currency||'SAR';
 $('amountReceived').value=Number(o.amountReceived||0);$('shippingCost').value=o.shippingCost||0;$('shippingCharge').value=o.shippingCharge||0;$('orderNotes').value=o.notes||'';
 $('items').innerHTML='';(o.items||[]).forEach(addItemRow);calcSummary();
}''',s,count=1,flags=re.S)
# Existing legacy payment controls must not be referenced by reset/edit or shown.
s=s.replace("const overdue=$('overdueDays');if(overdue)overdue.value=settings.overdueDays;", "const overdue=$('overdueDays');if(overdue)overdue.value=settings.overdueDays;")
s=s.replace("$('overdueDays').value=settings.overdueDays;", "if($('overdueDays'))$('overdueDays').value=settings.overdueDays;")
# Add native phone contact picker if present in the project.
if "$('pickContact').onclick" not in s:
 s=s.replace("$('nav').addEventListener('click'", """$('pickContact').onclick=async()=>{try{const p=window.Capacitor?.Plugins?.HisabatiContacts;if(!p?.pick){alert('دليل الهاتف غير متاح في هذه النسخة');return;}const r=await p.pick();if(r?.name)$('customerName').value=r.name;if(r?.phone)$('customerPhone').value=r.phone;}catch(e){if(!String(e?.message||e).toLowerCase().includes('cancel'))alert('تعذر اختيار جهة الاتصال');}};
$('nav').addEventListener('click'""",1)
# Keep the received amount and shipping totals reactive.
for line in ["$('shippingCost').addEventListener('input',calcSummary);","$('shippingCharge').addEventListener('input',calcSummary);","$('amountReceived').addEventListener('input',()=>{});"]:
 if line not in s:s=s.replace("$('addItem').onclick=()=>addItemRow();", "$('addItem').onclick=()=>addItemRow();\n"+line,1)
hp.write_text(h,encoding="utf-8");jp.write_text(s,encoding="utf-8")
print("Applied screenshot-led New Order screen with amount-only payment input")
