var elt = document.getElementById('produit');
elt.addEventListener('change', function () {
  console.log('value => '+this.value);

  // Mettre à jour le titre du tableau des informations de produit
  document.getElementById("infoTitle").innerHTML = `Info ${this.value.toUpperCase()}`;
  
  document.getElementById("kpiTitle").innerHTML = `${this.value.toUpperCase()}`;

  let formData = new FormData();
  formData.append('produit', this.value);

  // On récupère la valeur du jeton CSRF
  const request = new Request('/update-data/', {
      method: 'POST',
      body: formData,
  });

  // On exécute la requête
  fetch(request)
    .then(response => response.json())
    .then(result => {
          let info_ges = JSON.parse(result.info_ges);
          let info_non_ab = JSON.parse(result.info_non_ab);
          let resum = JSON.parse(result.resum_direction);
          let resum_graph = JSON.parse(result.resum_graph);
          let info_prod = JSON.parse(result.info_prod);
          
          gridOptionsGest.api.setRowData(info_ges);
          gridOptionsNonAb.api.setRowData(info_non_ab);
          gridOptionsResum.api.setRowData(resum);
          gridOptionsInfoProd.api.setRowData(info_prod);

          const optionsResume = {
            container: document.getElementById('resumeChart'),
            autoSize: true,
            data: resum_graph,
            theme: getResumeTheme(),
            series: getResumeSeries(),
            axes: getResumeAxes(),
            legend: getResumeLegend(),
          };
          agCharts.AgChart.update(chartResume, optionsResume);
          
          
          kpiData2 = [
            {
              name: 'Equipés',
              taux: info_prod[0].Equipement,
            },
            {
              name: 'Non Equipés',
              taux: 100 - info_prod[0].Equipement,
            },
          ];
          console.log(kpiData2[0].taux)
          const percentage = (value) => `${value}%`;
          const optionsKPI = {
            container: document.getElementById('kpi'),
            data: kpiData2,
            series: [
              {
                type: 'pie',
                angleKey: 'taux',
                fills: ['#E67900', '#dff3ea'],
                strokeWidth: 0,
                strokeOpacity: 0.7,
                highlightStyle: {
                  item : {
                    fill: '#d69f60'
                  },
                },
                innerRadiusOffset: -20,
                innerLabels: [
                  {
                    text: percentage(kpiData2[0].taux),
                    color: '#E67900',
                    fontSize: 25,
                  },
                  {
                    text: 'Equipés',
                    fontSize: 18,
                    margin: 4,
                  },
                ],
                innerCircle: {
                  fill: '#dff3ea',
                },
              },
            ],
          };
          agCharts.AgChart.update(kpiChart, optionsKPI);
          
          
          let evoProduit = JSON.parse(result.evo_produit);
          evoProduit.forEach(function(data) { data.Date = new Date(data.Date); });
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
})


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
// Fin

var eltDate = document.getElementById('idEditDate');
eltDate.addEventListener('change', function () {
  console.log('value => '+this.value);

  let urlcourante = document.location.href; 
  let formData = new FormData();
  formData.append('date', this.value);
  formData.append('url', urlcourante);

  // On récupère la valeur du jeton CSRF
  const request = new Request('/edit-date/', {
      method: 'POST',
      body: formData,
  });

  // On exécute la requête
  fetch(request)
  //   .then(response => response.json())
  //   .then(result => {
  //         // let info_ges = JSON.parse(result.info_ges);
          
  //         // gridOptionsGest.api.setRowData(info_ges);
  // })
})

