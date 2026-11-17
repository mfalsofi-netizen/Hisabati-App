from pathlib import Path
html = Path("www/index.html")
js = Path("www/app.js")
h = html.read_text(encoding="utf-8")
if 'id="printRoot"' not in h:
    css = """
#printRoot{display:none}
@media print{
  @page{margin:8mm}
  html,body{background:#fff!important;color:#111!important}
  body.printing>*:not(#printRoot){display:none!important}
  body.printing #printRoot{display:block!important;position:static!important;width:100%!important;color:#111!important;background:#fff!important}
  #printRoot *{visibility:visible!important;box-shadow:none!important}
  #printRoot table{width:100%!important;min-width:0!important;border-collapse:collapse!important;table-layout:fixed}
  #printRoot th,#printRoot td{border:1px solid #999!important;padding:5px 4px!important;font-size:10px!important;overflow-wrap:anywhere}
  #printRoot th{background:#eee!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  #printRoot .print-title{text-align:center;font-size:17px;margin:0 0 8px}
  #printRoot .print-meta{font-size:11px;line-height:1.8;margin:5px 0}
  #printRoot .print-section{margin-top:12px;break-inside:avoid}
  #printRoot tr{break-inside:avoid;page-break-inside:avoid}
  #printRoot .print-footer{margin-top:16px;text-align:center;color:#666;font-size:9px}
  body.printing.print-80mm #printRoot{width:72mm!important;margin:0 auto!important;font-family:Tahoma,Arial,sans-serif}
  body.printing.print-80mm #printRoot th,body.printing.print-80mm #printRoot td{font-size:9px!important;padding:4px 2px!important}
  body.printing.print-a4 @page{size:A4 portrait;margin:12mm}
}
"""
    h = h.replace("</style></head>", css + "</style></head>")
    h = h.replace("</main><footer>", '</main><div id="printRoot" aria-hidden="true"></div><footer>')
    html.write_text(h, encoding="utf-8")

s = js.read_text(encoding="utf-8")
anchor = "const today=()=>new Date().toISOString().slice(0,10);"
helper = """
function printDocument(title,content,format='a4'){
  const root=$('printRoot');
  if(!root){alert('تعذر تجهيز صفحة الطباعة');return;}
  if(document.body.classList.contains('printing'))return;
  root.innerHTML='<div class="print-title">حساباتي</div>'+content+'<div class="print-footer">برمجة وتطوير — مناف جلال</div>';
  document.title=title;
  document.body.classList.add('printing',format==='80mm'?'print-80mm':'print-a4');
  let finished=false, printStarted=false, failsafe;
  const cleanup=()=>{
    if(finished)return;
    finished=true;
    document.body.classList.remove('printing','print-80mm','print-a4');
    root.innerHTML='';
    document.title='حساباتي';
    window.removeEventListener('afterprint',cleanup);
    document.removeEventListener('visibilitychange',onVisible);
    clearTimeout(failsafe);
  };
  const onVisible=()=>{if(document.visibilityState==='visible'&&printStarted)setTimeout(cleanup,500);};
  window.addEventListener('afterprint',cleanup,{once:true});
  document.addEventListener('visibilitychange',onVisible);
  failsafe=setTimeout(cleanup,5*60*1000);
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    try{printStarted=true;window.print();}
    catch(e){cleanup();alert('تعذرت الطباعة: '+e.message);}
  }));
}
"""
if "function printDocument(" not in s:
    s = s.replace(anchor, anchor + "\n" + helper)

start = s.index("window.customerStatement=")
end = s.index("function renderExpenses()", start)
customer = """
window.customerStatement=(encoded)=>{
  let n=decodeURIComponent(encoded),a=orders.filter(o=>o.customerName===n);
  let sections=['SAR','USD'].map(c=>{
    let rows=a.filter(o=>o.currency===c);
    if(!rows.length)return '';
    return '<section class="print-section"><h3>كشف حساب — '+c+'</h3><table><thead><tr><th>رقم الطلب</th><th>التاريخ</th><th>الحالة</th><th>المبلغ المطلوب</th><th>صافي الربح</th></tr></thead><tbody>'+
      rows.map(o=>'<tr><td>'+esc(o.id)+'</td><td>'+esc(o.date)+'</td><td>'+esc(o.status)+'</td><td>'+money(totals(o).due,c)+'</td><td>'+money(totals(o).profit,c)+'</td></tr>').join('')+
      '</tbody></table></section>';
  }).join('');
  printDocument('كشف حساب العميل','<div class="print-meta"><b>كشف حساب العميل:</b> '+esc(n)+'<br>تاريخ الإصدار: '+today()+'</div>'+sections,'a4');
};
"""
s = s[:start] + customer + s[end:]

old_report = "$('runReport').onclick=report;$('printReport').onclick=()=>{if(!$('reportPrint'))report();window.print();};"
new_report = """$('runReport').onclick=report;
$('printReport').onclick=()=>{
  if(!$('reportPrint'))report();
  const el=$('reportPrint');
  if(!el)return;
  printDocument('تقرير الأرباح والمصاريف',el.innerHTML,'a4');
};"""
s = s.replace(old_report, new_report)

start = s.index("function printInvoice(id)")
end = s.index("window.printInvoice=printInvoice;", start)
invoice = """
function printInvoice(id){
  let o=orders.find(x=>x.id===id);if(!o)return;
  let t=totals(o);
  let rows=o.items.map(x=>'<tr><td>'+esc(x.name)+'<br><small>'+x.qty+' × '+money(x.price,o.currency)+'</small></td><td>'+money(x.qty*x.price,o.currency)+'</td></tr>').join('');
  let content='<div class="print-meta"><b>فاتورة طلب شراء</b><br>الحالة: '+esc(o.status)+'<br>رقم الطلب: '+esc(o.id)+'<br>التاريخ: '+esc(o.date)+'<br>العميل: '+esc(o.customerName)+'<br>'+(o.customerPhone?'الهاتف: '+esc(o.customerPhone):'')+'</div>'+
  '<section class="print-section"><table><thead><tr><th style="width:62%">الصنف</th><th>الإجمالي</th></tr></thead><tbody>'+rows+'</tbody></table></section>'+
  '<section class="print-section"><table><tbody><tr><td>إجمالي قيمة البضاعة</td><td>'+money(t.sale,o.currency)+'</td></tr><tr><td>الشحن المطلوب من العميل</td><td>'+money(t.sh,o.currency)+'</td></tr><tr><td><b>إجمالي المبلغ المطلوب</b></td><td><b>'+money(t.due,o.currency)+'</b></td></tr></tbody></table></section>'+
  (o.notes?'<p class="print-meta">ملاحظات: '+esc(o.notes)+'</p>':'');
  printDocument('فاتورة طلب شراء',content,'80mm');
}
"""
s = s[:start] + invoice + s[end:]
js.write_text(s, encoding="utf-8")
print("Print patch applied")
