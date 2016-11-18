var $table = $('body > table');
var $tr_list = $table.find('tr');
var router_list = [];
$tr_list.each(function(index){
     var $tr = $(this);
     var $td_list = $tr.find('td');
     var path_td = $td_list[1];
     if(!path_td){
         return;
     }
     var path = path_td.textContent.trim();
     if(!path.startsWith('/')){
         return;
     }
     var comment = $td_list[2].textContent.trim();
     comment = comment.replace(/[（(]/,'-');
     comment = comment.replace(/[)）]/,'');
     var router =  path+'(params,'+'c='+comment+')'+':get';
     router_list.push(router);
});

console.log(router_list.join('\n'));

