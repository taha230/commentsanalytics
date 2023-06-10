/*

=========================================================
* Volt Pro - Premium Bootstrap 5 Dashboard
=========================================================

* Product Page: https://themesberg.com/product/admin-dashboard/volt-bootstrap-5-dashboard
* Copyright 2021 Themesberg (https://www.themesberg.com)

* Designed and coded by https://themesberg.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. Please contact us to request a removal. Contact us if you want to remove it.

*/

"use strict";
const d = document;
d.addEventListener("DOMContentLoaded", function(event) {

    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-primary me-3',
            cancelButton: 'btn btn-gray'
        },
        buttonsStyling: false
    });

    var themeSettingsEl = document.getElementById('theme-settings');
    var themeSettingsExpandEl = document.getElementById('theme-settings-expand');

    if(themeSettingsEl) {

        var themeSettingsCollapse = new bootstrap.Collapse(themeSettingsEl, {
            show: true,
            toggle: false
        });

        if (window.localStorage.getItem('settings_expanded') === 'true') {
            themeSettingsCollapse.show();
            themeSettingsExpandEl.classList.remove('show');
        } else {
            themeSettingsCollapse.hide();
            themeSettingsExpandEl.classList.add('show');
        }
        
        themeSettingsEl.addEventListener('hidden.bs.collapse', function () {
            themeSettingsExpandEl.classList.add('show');
            window.localStorage.setItem('settings_expanded', false);
        });

        themeSettingsExpandEl.addEventListener('click', function () {
            themeSettingsExpandEl.classList.remove('show');
            window.localStorage.setItem('settings_expanded', true);
            setTimeout(function() {
                themeSettingsCollapse.show();
            }, 300);
        });
    }

    // options
    const breakpoints = {
        sm: 540,
        md: 720,
        lg: 960,
        xl: 1140
    };

    var sidebar = document.getElementById('sidebarMenu')
    if(sidebar && d.body.clientWidth < breakpoints.lg) {
        sidebar.addEventListener('shown.bs.collapse', function () {
            document.querySelector('body').style.position = 'fixed';
        });
        sidebar.addEventListener('hidden.bs.collapse', function () {
            document.querySelector('body').style.position = 'relative';
        });
    }

    var iconNotifications = d.querySelector('.notification-bell');
    if (iconNotifications) {
        iconNotifications.addEventListener('shown.bs.dropdown', function () {
            iconNotifications.classList.remove('unread');
        });
    }

    [].slice.call(d.querySelectorAll('[data-background]')).map(function(el) {
        el.style.background = 'url(' + el.getAttribute('data-background') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-background-lg]')).map(function(el) {
        if(document.body.clientWidth > breakpoints.lg) {
            el.style.background = 'url(' + el.getAttribute('data-background-lg') + ')';
        }
    });

    [].slice.call(d.querySelectorAll('[data-background-color]')).map(function(el) {
        el.style.background = 'url(' + el.getAttribute('data-background-color') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-color]')).map(function(el) {
        el.style.color = 'url(' + el.getAttribute('data-color') + ')';
    });

    //Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
    })


    // Popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl)
    })
    

    // Datepicker
    var datepickers = [].slice.call(d.querySelectorAll('[data-datepicker]'))
    var datepickersList = datepickers.map(function (el) {
        return new Datepicker(el, {
            buttonClass: 'btn'
          });
    })

    if(d.querySelector('.input-slider-container')) {
        [].slice.call(d.querySelectorAll('.input-slider-container')).map(function(el) {
            var slider = el.querySelector(':scope .input-slider');
            var sliderId = slider.getAttribute('id');
            var minValue = slider.getAttribute('data-range-value-min');
            var maxValue = slider.getAttribute('data-range-value-max');

            var sliderValue = el.querySelector(':scope .range-slider-value');
            var sliderValueId = sliderValue.getAttribute('id');
            var startValue = sliderValue.getAttribute('data-range-value-low');

            var c = d.getElementById(sliderId),
                id = d.getElementById(sliderValueId);

            noUiSlider.create(c, {
                start: [parseInt(startValue)],
                connect: [true, false],
                //step: 1000,
                range: {
                    'min': [parseInt(minValue)],
                    'max': [parseInt(maxValue)]
                }
            });
        });
    }

    if (d.getElementById('input-slider-range')) {
        var c = d.getElementById("input-slider-range"),
            low = d.getElementById("input-slider-range-value-low"),
            e = d.getElementById("input-slider-range-value-high"),
            f = [d, e];

        noUiSlider.create(c, {
            start: [parseInt(low.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
            connect: !0,
            tooltips: true,
            range: {
                min: parseInt(c.getAttribute('data-range-value-min')),
                max: parseInt(c.getAttribute('data-range-value-max'))
            }
        }), c.noUiSlider.on("update", function (a, b) {
            f[b].textContent = a[b]
        });
    }

    //Chartist

    if(d.querySelector('.ct-chart-requests-value')) {
        //Chart 5
        
        var $string_list_cleaned = d.getElementById('request_table').innerText.replace(/\'/g,"\"");
        var $data_input = JSON.parse("[" + JSON.parse($string_list_cleaned)["data"] + "]");
        var $month_input = JSON.parse($string_list_cleaned)["months"];
        // alert($month_input);

        new Chartist.Line('.ct-chart-requests-value', {
            labels: $month_input,
            series: [
                $data_input,
            ]
          }, {
            low: 0,
            showArea: true,
            fullWidth: true,
            plugins: [
              Chartist.plugins.tooltip()
            ],
            axisX: {
                // On the x-axis start means top and end means bottom
                position: 'end',
                showGrid: true
            },
            axisY: {
                // On the y-axis start means left and end means right
                showGrid: false,
                showLabel: false,
                labelInterpolationFnc: function(value) {
                    return '$' + (value / 1) + 'k';
                }
            }
        });
    }

    if(d.querySelector('.ct-chart-sales-value')) {
        //Chart 5
          new Chartist.Line('.ct-chart-sales-value', {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            series: [
                [0, 10, 30, 40, 80, 60, 100]
            ]
          }, {
            low: 0,
            showArea: true,
            fullWidth: true,
            plugins: [
              Chartist.plugins.tooltip()
            ],
            axisX: {
                // On the x-axis start means top and end means bottom
                position: 'end',
                showGrid: true
            },
            axisY: {
                // On the y-axis start means left and end means right
                showGrid: false,
                showLabel: false,
                labelInterpolationFnc: function(value) {
                    return '$' + (value / 1) + 'k';
                }
            }
        });
    }

    if(d.querySelector('.ct-chart-transactions-monthly')) {
        //Chart 5
        var $string_list_cleaned = d.getElementById('transaction_table').innerText.replace(/\'/g,"\"");;
        var $data_input = JSON.parse("[" + JSON.parse($string_list_cleaned)["data"] + "]");
        var $month_input = JSON.parse($string_list_cleaned)["months"];
      
        var chart = new Chartist.Bar('.ct-chart-transactions-monthly', {
            labels : $month_input,
            series: [
                $data_input,
            ]
          }, {
            low: 0,
            showArea: false,
            plugins: [
              Chartist.plugins.tooltip()
            ],
            axisX: {
                // On the x-axis start means top and end means bottom
                position: 'end'
            },
            axisY: {
                // On the y-axis start means left and end means right
                showGrid: true,
                showLabel: false,
                offset: 0
            }
            });
          
          chart.on('draw', function(data) {
            if(data.type === 'line' || data.type === 'area') {
              data.element.animate({
                d: {
                  begin: 5000 * data.index,
                  dur: 2000,
                  from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
                  to: data.path.clone().stringify(),
                  easing: Chartist.Svg.Easing.easeOutQuint
                }
              });
            }
        });
    }

    if(d.querySelector('.line-chart-bulk-sentiment')) {
        //Chart sentiment bulk

        var $string_list_cleaned = d.getElementById('sentiment_chart').innerText.replace(/\'/g,"\"");

        var $data_input_positive = JSON.parse("[" + JSON.parse($string_list_cleaned)["data_positive"] + "]");
        var $data_input_neutral = JSON.parse("[" + JSON.parse($string_list_cleaned)["data_neutral"] + "]");
        var $data_input_negative = JSON.parse("[" + JSON.parse($string_list_cleaned)["data_negative"] + "]");
        
        var $label_input = JSON.parse($string_list_cleaned)["labels"];

        var chart = new Chartist.Line('.line-chart-bulk-sentiment', {
                labels: $label_input,

                series: [
                    {
                        name: 'positive',
                        data: $data_input_positive
                    },
                    {
                        name: 'neutral',
                        data: $data_input_neutral
                    },
                    {
                        name: 'negative',
                        data: $data_input_negative
                    }
                ]
                }, {
                    
                fullWidth: true,
                chartPadding: {
                    right: 90,
                    left: 10
                },
                plugins: [
                    Chartist.plugins.tooltip()
                ],

                low: 0,
                high: 100,
                axisY: {
                    // Lets offset the chart a bit from the labels
                    offset: 60,
                    labelInterpolationFnc: function(value) {
                      return value + ' %';
                    }
                  },
                  series: {
                    'positive': {
                    },
                    'neutral': {
                    },
                    'negative': {
                    }
                  }
                
                  
        });

        chart.on('draw', function(data) {
            if(data.type === 'line' || data.type === 'area') {
              data.element.animate({
                d: {
                  begin: 2000 * data.index,
                  dur: 2000,
                  from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
                  to: data.path.clone().stringify(),
                  easing: Chartist.Svg.Easing.easeOutQuint
                }
              });
            }
          });

    }

    if(d.querySelector('.bar-chart-horizontal-bulk-ner-top-count')) {
        //Chart sentiment bulk

        var $string_list_cleaned = d.getElementById('bar_chart_top_count').innerText.replace(/\'/g,"\"");
        var $data_input_ner_count = JSON.parse("[" + JSON.parse($string_list_cleaned)["data_count"] + "]");

        
        var $label_input = JSON.parse($string_list_cleaned)["labels"];
        
        // alert($string_list_cleaned);

        var options_ner_bar_chart_count = {
            series: [{
            name : 'count',
            data: $data_input_ner_count
          }],
            chart: {
            type: 'bar',
            height: 320,
            width: '100%',
            float: 'right'
          },
          legend: {
            show: false
          },
          title: {
            text: 'Items Count   '
          },
          plotOptions: {
            bar: {
              borderRadius: 10,
              horizontal: true,
              distributed: true,
        
            }
          },
          colors: ['#058fff', '#ff058a', '#05ff37', '#ebf211', '#f50505', '#8366e3', '#05f2d3', '#97fa34',
                  '#f48024', '#3c02fa'
                ],
          
          
          xaxis: {
            categories: $label_input,
          }
          };
        
        var barchart_ner_count = new ApexCharts(d.querySelector(".bar-chart-horizontal-bulk-ner-top-count"), options_ner_bar_chart_count);
        barchart_ner_count.render();
        
    }
    
    if(d.querySelector('.bar-chart-horizontal-bulk-ner-top-sentiment')) {
        //Chart sentiment bulk

        var $string_list_cleaned = d.getElementById('bar_chart_top_count').innerText.replace(/\'/g,"\"");
        var $data_input_ner_count = JSON.parse("[" + JSON.parse($string_list_cleaned)["data_count"] + "]");

        
        var $label_input = JSON.parse($string_list_cleaned)["labels"];
        var $positive_input = JSON.parse($string_list_cleaned)["data_positive"];
        var $neutral_input = JSON.parse($string_list_cleaned)["data_neutral"];
        var $negative_input = JSON.parse($string_list_cleaned)["data_negative"];
        
        // alert($string_list_cleaned);

        var options_ner_bar_chart_sentiment = {
            series: [{
                name: 'Postivie',
                data: $positive_input
              }, {
                name: 'Neutral',
                data: $neutral_input
              }, {
                name: 'Negative',
                data: $negative_input
              }],
                chart: {
                type: 'bar',
                height: 350,
                width: '100%',
                stacked: true,
                stackType: '100%'
              },
              plotOptions: {
                bar: {
                  horizontal: true,
                },
                
              },
              colors: ['#2de004', '#d6d604', '#d60424'],

              stroke: {
                width: 1,
                colors: ['#fff']
              },
              title: {
                text: 'Sentiment Per Items'
              },
              xaxis: {
                categories: $label_input,
              },
              tooltip: {
                y: {
                  formatter: function (val) {
                    return val + ""
                  }
                }
              },
              fill: {
                opacity: 1
              
              },
              legend: {
                position: 'bottom',
                horizontalAlign: 'left',
                offsetX: 40
              }
              };
        
        var barchart_ner_sentiment = new ApexCharts(d.querySelector(".bar-chart-horizontal-bulk-ner-top-sentiment"), options_ner_bar_chart_sentiment);
        barchart_ner_sentiment.render();
        
    }

    if(d.querySelector('.bar-chart-horizontal-bulk-keyword-top-sentiment')) {
      //Chart sentiment bulk

      var $string_list_cleaned = d.getElementById('bar_chart_top_count').innerText.replace(/\'/g,"\"");
      var $data_input_keyword_count = JSON.parse("[" + JSON.parse($string_list_cleaned)["data_count"] + "]");

      
      var $label_input = JSON.parse($string_list_cleaned)["labels"];
      var $positive_input = JSON.parse($string_list_cleaned)["data_positive"];
      var $neutral_input = JSON.parse($string_list_cleaned)["data_neutral"];
      var $negative_input = JSON.parse($string_list_cleaned)["data_negative"];
      
      // alert($string_list_cleaned);

      var options_keyword_bar_chart_sentiment = {
          series: [{
              name: 'Postivie',
              data: $positive_input
            }, {
              name: 'Neutral',
              data: $neutral_input
            }, {
              name: 'Negative',
              data: $negative_input
            }],
              chart: {
              type: 'bar',
              height: 350,
              width: '100%',
              stacked: true,
              stackType: '100%'
            },
            plotOptions: {
              bar: {
                horizontal: true,
              },
              
            },
            colors: ['#2de004', '#d6d604', '#d60424'],

            stroke: {
              width: 1,
              colors: ['#fff']
            },
            title: {
              text: 'Sentiment Per Keyword'
            },
            xaxis: {
              categories: $label_input,
            },
            tooltip: {
              y: {
                formatter: function (val) {
                  return val + ""
                }
              }
            },
            fill: {
              opacity: 1
            
            },
            legend: {
              position: 'bottom',
              horizontalAlign: 'left',
              offsetX: 40
            }
            };
      
      var barchart_keyword_sentiment = new ApexCharts(d.querySelector(".bar-chart-horizontal-bulk-keyword-top-sentiment"), options_keyword_bar_chart_sentiment);
      barchart_keyword_sentiment.render();
      
    }

    if(d.querySelector('.myChart_wordcloud')) {

      // wordcloud 
      var $string_list_cleaned = d.getElementById('wordcloud_chart').innerText.replace(/\'/g,"\"");
      var $data_input_wordcloud = JSON.parse($string_list_cleaned);

      
      // alert(JSON.parse($string_list_cleaned)[0]['text']);
      var myConfig = {
        "graphset":[
        {
        "type":"wordcloud",
        "options":{
          "style":{
            "tooltip":{
              visible: true,
              text: '%text: %hits'
            }
          },
        "words": $data_input_wordcloud,
            }
          }
          ]
        };
        
        zingchart.render({ 
          id: 'myChart_wordcloud', 
          data: myConfig, 
          height: '50%', // Set to 100% to fully scale to parent container
          width: '55%', 
        });      
    }

    if(d.querySelector('.bar-chart-horizontal-bulk-keyword-top-count')) {
      //Chart sentiment bulk

      var $string_list_cleaned = d.getElementById('bar_chart_top_count').innerText.replace(/\'/g,"\"");
      var $data_input_keyword_count = JSON.parse("[" + JSON.parse($string_list_cleaned)["data_count"] + "]");

      
      var $label_input = JSON.parse($string_list_cleaned)["labels"];
      
      // alert($string_list_cleaned);

      var options_keyword_bar_chart_count = {
          series: [{
          name : 'count',
          data: $data_input_keyword_count
        }],
          chart: {
          type: 'bar',
          height: 320,
          width: '100%',
          float: 'right'
        },
        legend: {
          show: false
        },
        title: {
          text: 'Keyword Count   '
        },
        plotOptions: {
          bar: {
            borderRadius: 10,
            horizontal: true,
            distributed: true,
      
          }
        },
        colors: ['#058fff', '#ff058a', '#05ff37', '#ebf211', '#f50505', '#8366e3', '#05f2d3', '#97fa34',
                '#f48024', '#3c02fa'
              ],
        
        
        xaxis: {
          categories: $label_input,
        }
        };
      
      var barchart_keyword_count = new ApexCharts(d.querySelector(".bar-chart-horizontal-bulk-keyword-top-count"), options_keyword_bar_chart_count);
      barchart_keyword_count.render();
      
  }

    if(d.querySelector('.ct-chart-ranking')) {
        var chart = new Chartist.Bar('.ct-chart-ranking', {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            series: [
              [1, 5, 2, 5, 4, 3],
              [2, 3, 4, 8, 1, 2],
            ]
          }, {
            low: 0,
            showArea: true,
            plugins: [
              Chartist.plugins.tooltip()
            ],
            axisX: {
                // On the x-axis start means top and end means bottom
                position: 'end'
            },
            axisY: {
                // On the y-axis start means left and end means right
                showGrid: false,
                showLabel: false,
                offset: 0
            }
            });
          
          chart.on('draw', function(data) {
            if(data.type === 'line' || data.type === 'area') {
              data.element.animate({
                d: {
                  begin: 2000 * data.index,
                  dur: 2000,
                  from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
                  to: data.path.clone().stringify(),
                  easing: Chartist.Svg.Easing.easeOutQuint
                }
              });
            }
        });
    }

    if(d.querySelector('.ct-chart-traffic-share')) {
        var data = {
            series: [70, 20, 10]
          };
          
          var sum = function(a, b) { return a + b };
          
          new Chartist.Pie('.ct-chart-traffic-share', data, {
            labelInterpolationFnc: function(value) {
              return Math.round(value / data.series.reduce(sum) * 100) + '%';
            },            
            low: 0,
            high: 8,
            donut: true,
            donutWidth: 20,
            donutSolid: true,
            fullWidth: false,
            showLabel: false,
            plugins: [
              Chartist.plugins.tooltip()
            ],
        });         
    }

    if (d.getElementById('loadOnClick')) {
        d.getElementById('loadOnClick').addEventListener('click', function () {
            var button = this;
            var loadContent = d.getElementById('extraContent');
            var allLoaded = d.getElementById('allLoadedText');
    
            button.classList.add('btn-loading');
            button.setAttribute('disabled', 'true');
    
            setTimeout(function () {
                loadContent.style.display = 'block';
                button.style.display = 'none';
                allLoaded.style.display = 'block';
            }, 1500);
        });
    }

    var scroll = new SmoothScroll('a[href*="#"]', {
        speed: 500,
        speedAsDuration: true
    });

    if(d.querySelector('.current-year')){
        d.querySelector('.current-year').textContent = new Date().getFullYear();
    }

    // Glide JS

    if (d.querySelector('.glide')) {
        new Glide('.glide', {
            type: 'carousel',
            startAt: 0,
            perView: 3
          }).mount();
    }

    if (d.querySelector('.glide-testimonials')) {
        new Glide('.glide-testimonials', {
            type: 'carousel',
            startAt: 0,
            perView: 1,
            autoplay: 2000
          }).mount();
    }

    if (d.querySelector('.glide-clients')) {
        new Glide('.glide-clients', {
            type: 'carousel',
            startAt: 0,
            perView: 5,
            autoplay: 2000
          }).mount();
    }

    if (d.querySelector('.glide-news-widget')) {
        new Glide('.glide-news-widget', {
            type: 'carousel',
            startAt: 0,
            perView: 1,
            autoplay: 2000
          }).mount();
    }

    if (d.querySelector('.glide-autoplay')) {
        new Glide('.glide-autoplay', {
            type: 'carousel',
            startAt: 0,
            perView: 3,
            autoplay: 2000
          }).mount();
    }

    // Pricing countup
    var billingSwitchEl = d.getElementById('billingSwitch');
    if(billingSwitchEl) {
        const countUpStandard = new countUp.CountUp('priceStandard', 99, { startVal: 199 });
        const countUpPremium = new countUp.CountUp('pricePremium', 199, { startVal: 299 });
        
        billingSwitchEl.addEventListener('change', function() {
            if(billingSwitch.checked) {
                countUpStandard.start();
                countUpPremium.start();
            } else {
                countUpStandard.reset();
                countUpPremium.reset();
            }
        });
    }

});

// Line chart
var optionsLineChart = {
    series: [{
        name: 'Clients',
        data: [120, 160, 200, 470, 420, 150, 470, 750, 650, 190, 140]
    }],
    labels: ['01 Feb', '02 Feb', '03 Feb', '04 Feb', '05 Feb', '06 Feb', '07 Feb', '08 Feb', '09 Feb', '10 Feb', '11 Feb'],
    chart: {
        type: 'area',
        width: "100%",
        height: 360
    },
    theme: {
        monochrome: {
            enabled: true,
            color: '#31316A',
        }
    },
    tooltip: {
        fillSeriesColor: false,
        onDatasetHover: {
            highlightDataSeries: false,
        },
        theme: 'light',
        style: {
            fontSize: '12px',
            fontFamily: 'Inter',
        },
    },
};


// DataTables
var dataTableEl = d.getElementById('datatable-searchable');
if (dataTableEl) {
    const dataTable = new simpleDatatables.DataTable(dataTableEl);
}



