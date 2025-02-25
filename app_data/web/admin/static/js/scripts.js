
// שיטה לקיצור בחירת אלמנטים
function $(selector) {
  return document.querySelector(selector);
}

function find(el, selector) {
  return el ? el.querySelector(selector) : null;
}

function siblings(el) {
  if (!el || !el.parentNode) return [];
  const siblings = [];
  for (let sibling of el.parentNode.children) {
    if (sibling !== el) {
      siblings.push(sibling);
    }
  }
  return siblings;
}

// בחירת אלמנטים חשובים
const showAsideBtn = $('.show-side-btn');
const sidebar = $('.sidebar');
const wrapper = $('#wrapper');

if (showAsideBtn) {
  showAsideBtn.addEventListener('click', function () {
    const target = $(`#${this.dataset.show}`);
    if (target) {
      target.classList.toggle('show-sidebar');
      wrapper.classList.toggle('fullwidth');
    }
  });
}

// הצגת sidebar במסכים קטנים
if (window.innerWidth < 767) {
  if (sidebar) sidebar.classList.add('show-sidebar');
}

// ניהול שינויי גודל חלון
window.addEventListener('resize', function () {
  if (window.innerWidth > 767) {
    if (sidebar) sidebar.classList.remove('show-sidebar');
  }
});

// dropdown menu ב-side nav
const sidebarCategories = $('.sidebar .categories');
if (sidebarCategories) {
  sidebarCategories.addEventListener('click', function (event) {
    event.preventDefault();

    const item = event.target.closest('.has-dropdown');
    if (!item) return;

    item.classList.toggle('opened');
    siblings(item).forEach(sibling => sibling.classList.remove('opened'));

    if (item.classList.contains('opened')) {
      const toOpen = find(item, '.sidebar-dropdown');
      if (toOpen) toOpen.classList.add('active');

      siblings(item).forEach(sibling => {
        const toClose = find(sibling, '.sidebar-dropdown');
        if (toClose) toClose.classList.remove('active');
      });
    } else {
      const activeDropdown = find(item, '.sidebar-dropdown');
      if (activeDropdown) activeDropdown.classList.toggle('active');
    }
  });
}

// סגירת sidebar
const closeAsideBtn = $('.sidebar .close-aside');
if (closeAsideBtn) {
  closeAsideBtn.addEventListener('click', function () {
    const target = $(`#${this.dataset.close}`);
    if (target) target.classList.add('show-sidebar');
    wrapper.classList.remove('margin');
  });
}

/* 
  ===== Updated defaults for Chart.js 3+ or 4+ =====
  Removed all "Chart.defaults.global" references 
  and replaced them with the new structure.
*/

// Animation
Chart.defaults.animation.duration = 2000;

// Titles
Chart.defaults.plugins.title.display = false;

// Fonts & colors
Chart.defaults.color = '#71748c';
Chart.defaults.font.size = 13;

// Tooltips
Chart.defaults.plugins.tooltip.backgroundColor = '#111827';
Chart.defaults.plugins.tooltip.borderColor = 'blue';

// Legend
Chart.defaults.plugins.legend.labels.padding = 0;
Chart.defaults.plugins.legend.display = false;

// Points
Chart.defaults.elements.point.radius = 0;

// Responsiveness
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = false;

/* 
  Grid & Tick defaults for category (x-axis) 
  and linear (y-axis) scales 
*/
Chart.defaults.scales.category.grid.color = '#3b3d56';
Chart.defaults.scales.category.grid.borderColor = '#3b3d56';
Chart.defaults.scales.category.grid.drawBorder = false;
Chart.defaults.scales.category.ticks.color = '#71748c';
Chart.defaults.scales.category.ticks.font = { size: 12 };
Chart.defaults.scales.category.ticks.padding = 10;

Chart.defaults.scales.linear.grid.color = '#3b3d56';
Chart.defaults.scales.linear.grid.borderColor = '#3b3d56';
Chart.defaults.scales.linear.grid.drawBorder = false;
Chart.defaults.scales.linear.ticks.color = '#71748c';
Chart.defaults.scales.linear.ticks.font = { size: 12 };
Chart.defaults.scales.linear.ticks.padding = 10;
Chart.defaults.scales.linear.beginAtZero = false;

// הגדרת גרף עמודות
new Chart(document.getElementById('myChart'), {
  type: 'bar',
  data: {
    labels: ["January", "February", "March", "April", "May", "June", "August", "September"],
    datasets: [
      {
        label: "Lost",
        data: [45, 25, 40, 20, 60, 20, 35, 25],
        backgroundColor: "#0d6efd",
        borderColor: 'transparent',
        borderWidth: 2.5,
        barPercentage: 0.4,
      },
      {
        label: "Success",
        data: [20, 40, 20, 50, 25, 40, 25, 10],
        backgroundColor: "#dc3545",
        borderColor: 'transparent',
        borderWidth: 2.5,
        barPercentage: 0.4,
      }
    ]
  },
  options: {
    scales: {
      y: {
        // For Chart.js 3+, yAxes -> y
        ticks: { stepSize: 15 },
      },
      x: {
        // For Chart.js 3+, xAxes -> x
        grid: { display: false },
      }
    }
  }
});


new Chart(document.getElementById('myChart2'), {
  type: 'line',
  data: {
    labels: ["January", "February", "March", "April", "May", "June", "August", "September"],
    datasets: [
      {
        label: "Dataset 1",
        data: [4, 20, 5, 20, 5, 25, 9, 18],
        borderColor: '#0d6efd',
        lineTension: 0.4,
        borderWidth: 1.5,
      },
      {
        label: "Dataset 2",
        data: [11, 25, 10, 25, 10, 30, 14, 23],
        borderColor: '#dc3545',
        lineTension: 0.4,
        borderWidth: 1.5,
      },
      {
        label: "Dataset 3",
        data: [16, 30, 16, 30, 16, 36, 21, 35],
        borderColor: '#f0ad4e',
        lineTension: 0.4,
        borderWidth: 1.5,
      }
    ]
  },
  options: {
    scales: {
      y: {
        ticks: { stepSize: 12 },
      },
      x: {
        grid: { display: false },
      }
    }
  }
});

// גרף נוסף
new Chart(document.getElementById('chart3'), {
  type: 'line',
  data: {
    labels: ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"],
    datasets: [
      {
        label: "Lost",
        data: [3, 30, 16, 30, 16, 36, 21, 40, 20, 30],
        borderColor: '#d9534f',
        lineTension: 0.2,
        borderWidth: 1.5,
      },
      {
        label: "Won",
        data: [6, 20, 5, 20, 5, 25, 9, 18, 20, 15],
        borderColor: '#5cb85c',
        lineTension: 0.2,
        borderWidth: 1.5,
      }
    ]
  },
  options: {
    scales: {
      y: {
        ticks: { stepSize: 12 },
      },
      x: {
        grid: { display: false },
      }
    }
  }
});


function Send_POST_Test(){
  var url = "http://localhost:3000/api/PostTest";
  var data = {name: "John Doe", age: 30};
  fetch(url, {
    method: 'POST', 
    body: JSON.stringify(data), 
    headers:{
      'Content-Type': 'application/json'
    }
  }).then(res => res.json())
  .then(response => console.log('Success:', JSON.stringify(response)))
  .catch(error => console.error('Error:', error));


}
