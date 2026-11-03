(function(){
var LAT0=40.625,LAT1=40.782,LON0=-74.085,LON1=-73.862,W=1000,H=Math.round(W*(LAT1-LAT0)/((LON1-LON0)*Math.cos(40.72*Math.PI/180)));
var NS='http://www.w3.org/2000/svg',SRC='https://tile.openstreetmap.org/{z}/{x}/{y}.png';
function X(lon){return (lon-LON0)/(LON1-LON0)*W;}
function Y(lat){return (LAT1-lat)/(LAT1-LAT0)*H;}
function draw(svg){
  var g=svg.querySelector('.tiles');if(!g)return;
  var vb=svg.viewBox.baseVal,w=svg.getBoundingClientRect().width;if(!w)return;
  var lonA=LON0+vb.x/W*(LON1-LON0),lonB=LON0+(vb.x+vb.width)/W*(LON1-LON0);
  var latA=LAT1-vb.y/H*(LAT1-LAT0),latB=LAT1-(vb.y+vb.height)/H*(LAT1-LAT0);
  var z=Math.max(11,Math.min(18,Math.round(Math.log2(360*w/((lonB-lonA)*256))+1))),n=Math.pow(2,z);
  function tx(lon){return Math.floor((lon+180)/360*n);}
  function ty(lat){var r=lat*Math.PI/180;return Math.floor((1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2*n);}
  function lon(x){return x/n*360-180;}
  function lat(y){var m=Math.PI-2*Math.PI*y/n;return 180/Math.PI*Math.atan(0.5*(Math.exp(m)-Math.exp(-m)));}
  var x0=tx(lonA),x1=tx(lonB),y0=ty(latA),y1=ty(latB);
  if((x1-x0+1)*(y1-y0+1)>120)return;
  var want={},pending=0;
  function sweep(){if(pending>0)return;[].slice.call(g.children).forEach(function(im){if(!want[im.dataset.k])g.removeChild(im);});}
  for(var tX=x0;tX<=x1;tX++)for(var tY=y0;tY<=y1;tY++){
    var k=z+'/'+tX+'/'+tY;want[k]=1;
    if(g.querySelector('[data-k="'+k+'"]'))continue;
    var im=document.createElementNS(NS,'image'),ix=X(lon(tX)),iy=Y(lat(tY)),iw=X(lon(tX+1))-ix,ih=Y(lat(tY+1))-iy;
    im.dataset.k=k;im.setAttribute('x',ix);im.setAttribute('y',iy);im.setAttribute('width',iw*1.004);im.setAttribute('height',ih*1.004);
    im.setAttribute('preserveAspectRatio','none');pending++;
    im.addEventListener('load',function(){pending--;svg.classList.add('has-tiles');sweep();});
    im.addEventListener('error',function(){pending--;sweep();});
    im.setAttribute('href',SRC.replace('{z}',z).replace('{x}',tX).replace('{y}',tY));
    g.appendChild(im);
  }
  sweep();
}
function watch(svg){
  var t;function later(){clearTimeout(t);t=setTimeout(function(){draw(svg);},150);}
  new MutationObserver(later).observe(svg,{attributes:true,attributeFilter:['viewBox']});
  window.addEventListener('resize',later);
  if('IntersectionObserver' in window)new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)draw(svg);});}).observe(svg);
  else draw(svg);
}
document.querySelectorAll('svg.dmap,svg#tripmap').forEach(watch);
})();
