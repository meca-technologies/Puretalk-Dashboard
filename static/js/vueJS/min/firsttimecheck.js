function _0x24aa(a,t){var n=_0x256a();return(_0x24aa=function(a,t){return n[a-=374]})(a,t)}function _0x256a(){var a=["style","parent","/import-leads","522wFxvSx","attr","notif-badge","/form-builder","#notification-body","14693250FnNEdi","184lqDsvt","6318880kOUUXZ","pathname","8813529QkuXRu","length","2787111hNppww","display","1351998qveUIi","#notif-badge","21PXbsCT","get","lead_length","notifications","log","69385VguqNe","2102PyttOL","campaign_length","location"];return(_0x256a=function(){return a})()}var _0x5f0da6=_0x24aa;!function(){for(var a=_0x24aa,t=_0x256a();;)try{if(634110==+parseInt(a(376))*(parseInt(a(382))/2)+-parseInt(a(393))/3+-parseInt(a(388))/4*(-parseInt(a(375))/5)+parseInt(a(395))/6*(parseInt(a(397))/7)+-parseInt(a(389))/8+-parseInt(a(391))/9+parseInt(a(387))/10)break;t.push(t.shift())}catch(a){t.push(t.shift())}}();var notifications=new Vue({delimiters:["[[","]]"],el:_0x5f0da6(386),data:{notifications:{},length:0}});function updateNotification(){var e=_0x5f0da6;$[e(398)]("/api/v1/companies/first-time",function(a){var t=e;console[t(374)](a);var n=0,i=!0;0==a.form_length?(n+=1,t(385)==window[t(378)].pathname&&(i=!1)):0==a[t(377)]?(n+=1,"/campaigns"==window.location.pathname&&(i=!1)):0==a[t(399)]&&(n+=1,t(381)==window[t(378)][t(390)]&&(i=!1)),notifications[t(400)]=a,0<(notifications[t(392)]=n)&&i&&"false"==$(t(396))[t(380)]()[t(383)]("aria-expanded")&&$("#notif-badge").click(),document.getElementById(t(384))[t(379)][t(394)]=""})}updateNotification();