// Valeur initial pour la date de selection
let dateControl = document.querySelector('#periode');
dateControl.value = new Date().toJSON().slice(0, 10);
dateControl.max = new Date().toJSON().slice(0, 10);
// Fin Valeur


// Choisir une periode à comparer
var eltPeriode = document.querySelector('#periode');
eltPeriode.addEventListener('change', function () {
 console.log('value => '+this.value);

 let formPeriode = new FormData();
  formPeriode.append('periode', this.value);
  const requestPeriode = new Request('/synthese-update-compa-data/', {
    method: 'POST',
    body: formPeriode,
  });

  fetch(requestPeriode)
      .then(response => response.json())
      .then(result => {
          let data = JSON.parse(result.data);
          gridOptionsData.api.setRowData(data);
  })

});


// Choisir un produit
var eltProduit = document.querySelector('#produit');
eltProduit.addEventListener('change', function () {
 console.log('value => '+this.value);

 let formProduit = new FormData();
  formProduit.append('produit', this.value);
  const requestProduit = new Request('/synthese-update-prod/', {
    method: 'POST',
    body: formProduit,
  });

  fetch(requestProduit)
      .then(response => response.json())
      .then(result => {
          let evoProduit = JSON.parse(result.evo_produit);
          evoProduit.forEach(function(data) { data.Date = new Date(data.Date); });
          console.log(evoProduit);
          
          const optionsEvoProd = {
            container: document.getElementById('idEvoProd'),
            autoSize: true,
            data: evoProduit,
            theme: getEvoProdTheme(),
            series: getEvoProdSeries(),
            axes: getEvoProdAxes(),
            legend: getEvoProdLegend(),
          };
          agCharts.AgChart.update(chartEvoProd, optionsEvoProd);
  })

});