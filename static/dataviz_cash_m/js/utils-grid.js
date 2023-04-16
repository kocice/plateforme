// Valeur initial pour la date de selection
let dateControl = document.querySelector('#periode');
dateControl.value = new Date().toJSON().slice(0, 10);
dateControl.max = new Date().toJSON().slice(0, 10);
// Fin Valeur


const cellClassRules = {
    "row-rouge ": params => params.value < 15 && params.data.Cible > 0,
    "row-orange": params => params.value >= 15 && params.value < 30,
    "row-ras": params => params.value >= 30 && params.value < 60,
    "row-vert-ciel": params => params.value >= 60 && params.value < 85,
    "row-vert": params => params.value > 85
};

const cellClassRulesProd = {
    "prod-rouge ": params => params.value < 15 && params.data.Cible > 0,
    "prod-orange": params => params.value >= 15 && params.value < 30,
    "prod-ras": params => params.value >= 30 && params.value < 60,
    "prod-vert-ciel": params => params.value >= 60 && params.value < 85,
    "prod-vert": params => params.value > 85
};

const cellClassRulesNormale = {
    "row-ras": params => params.value >= 0,
};


// Parametres du graph de resumé de produit
function getResumeLegend() {
  const resumeLegend = {
    position: 'bottom',
    item: {
      marker: {
        shape: 'square',
        strokeWidth: 0,
      },
    },
  }   
  return resumeLegend;
}

function getResumeAxes() {
  const resumeAxes = [
    {
      type: 'category',
      position: 'bottom',
    },
    {
      type: 'number',
      position: 'left',
      keys: ['abonne', 'cible'],
      label: {
        formatter: (params) => {
          return params.value + ' ';
        },
      },
    },
    {
      type: 'number',
      position: 'right',
      keys: ['equipement'],
      label: {
        formatter: (params) => {
          return params.value + '%';
        },
      },
    },
  ]
  return resumeAxes;
}

function getResumeSeries() {
  const resumeSeries = [
    {
      type: 'column',
      xKey: 'directions',
      yKey: 'abonne',
      yName: 'Abonné',
      label: {
        formatter: (params) => {
          return params.value.toFixed(0);
        },
        color: "#46484D",
        fontWeight: "600",
        placement: "outside"
      },
    },
    {
      type: 'column',
      xKey: 'directions',
      yKey: 'cible',
      yName: 'Cible',
      label: {
        formatter: (params) => {
          return params.value.toFixed(0);
        },
        color: "#46484D",
        fontWeight: "600",
        placement: "outside"
      },
    },
    {
      type: 'line',
      xKey: 'directions',
      yKey: 'equipement',
      yName: '% Equipement',
      strokeWidth: 2,
      label: {
        fontWeight: 'bold',
      },
    },
  ]
  return resumeSeries;
}

function getResumeTheme() {
  const resumeTheme = {
    palette: {
      fills: ['#E67900', '#491E06', '#80a0c3'],
      strokes: ['#c16068', '#a2bf8a', '#80a0c3'],
    },
    overrides: {
      column: { series: { 
        strokeWidth: 0,
        strokeOpacity: 0.7,
        highlightStyle: {
          item : {
            fill: '#e0ab6eb7'
          }
        } 
      } },
      line: { 
        series: {
          strokeWidth: 5,
          marker: {
            enabled: false,
            fill: '#80a0c3',
            stroke: '#E67900'
          },
          //label: {
          //  enabled: true,
          //  fontWeight: 'bold'
          //}
        } 
      },
    },
  } 
  return resumeTheme;
}
// Fin


// Parametres du graph evolution de produit (synthese)
function getEvoProdLegend() {
  const evoProdLegend = {
    position: 'bottom',
  }
  return evoProdLegend;
}

function getEvoProdAxes() {
  const evoProdAxes = [
    {
      type: 'time',
      position: 'bottom',
      label: {
        format: '%b',
      },
    },
    {
      type: 'number',
      position: 'left',
      keys: ['Abonne'],
      title: {
        text: 'Abonnés',
      },
      label: {
        formatter: (params) => {
          return params.value  + ' ';
        },
      },
    },
    {
      type: 'number',
      position: 'right',
      keys: ['Croissance', 'Equipement'],
      label: {
        formatter: (params) => {
          return params.value + '%';
        },
      },
    },
  ]
  return evoProdAxes;
}

function getEvoProdSeries() {
  const evoProdSeries = [
    { 
      type: 'area', 
      xKey: 'Date',
      stacked: true, 
      yKey: 'Abonne',
      yName: 'Abonnés',
    },
    {
      type: 'line',
      xKey: 'Date',
      yKey: 'Equipement',
      yName: 'Equipement',
    },
    {
      type: 'line',
      xKey: 'Date',
      yKey: 'Croissance',
      yName: 'Croissance',
    },
  ]
  return evoProdSeries;
}

function getEvoProdTheme() {
  const evoProdTheme = {
    palette: {
      fills: ['#5BC0EB', '#E67900', '#46484D'],
      strokes: ['#4086a4', '#b1a235', '#6c8a2b'],
    },
    overrides: {
      area: {
        series: {
          marker: { enabled: true },
          highlightStyle: {
            series: {
              dimOpacity: 0.2,
            },
          },
        },
      },
    },
  }
  return evoProdTheme;
}
