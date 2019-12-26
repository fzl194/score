$(function() {
    "use strict";
    // Dashboard 1 Morris-chart
	Morris.Bar({
        element: 'total_bar',
        data: [{
            label: '< 60',
            No: 3,
        }, {
            label: '60 ~ 64',
            No: 4,
        }, { 
            label: '65 ~ 69',
            No: 5,
        }, {
            label: '70 ~ 74',
            No: 6,
        }, {
            label: '75 ~ 79',
            No: 10,
		}, {
            label: '80 ~ 84',
            No: 9,
		}, {
            label: '85 ~ 89',
            No: 7,
		}, {
            label: '90 ~ 94',
            No: 3,
		}, {
            label: '95 ~ 100',
            No: 1,
        }],
        xkey: 'label',
        ykeys: ['No'],
        labels: ['No'],
        pointSize: 0,
        fillOpacity: 0,
        pointStrokeColors: [ '#009efb','#7460ee'],
        behaveLikeLine: true,
        gridLineColor: '#f6f6f6',
        lineWidth: 1,
        hideHover: 'auto',
		barColors: ['#0099ff'],
        resize: true
    });
	
    Morris.Bar({
        element: 'que_bar',
        data: [{
            label: '1',
            Score: 1,
        }, {
            label: '2',
            Score: 2,
        }, {
            label: '3',
            Score: 4,
        }, {
            label: '4',
            Score: 6,
        }, {
            label: '5',
            Score: 8,
        }, {
            label: '6',
            Score: 9,
        }, {
            label: '7',
            Score: 7,
		}, {
            label: '8',
            Score: 4,
        }, {
            label: '9',
            Score: 3,
        }, {
            label: '10',
            Score: 1,
        }],
        xkey: 'label',
        ykeys: ['Score'],
        labels: ['Score'],
        pointSize: 0,
        fillOpacity: 0,
        pointStrokeColors: [ '#009efb','#7460ee'],
        behaveLikeLine: true,
        gridLineColor: '#f6f6f6',
        lineWidth: 1,
        hideHover: 'auto',
		barColors: ['#0099ff'],
        resize: true
    });

});