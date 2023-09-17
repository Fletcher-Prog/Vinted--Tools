
const url='http://127.0.0.1:3003/vinted?https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first';

async function url_down(){
   const res = await fetch(url);
   let data = await res.json();
   console.log(data);
   return data;
};
 
 
let data8 = url_down(); 
typeof data8;
console.log(data8[0]);



