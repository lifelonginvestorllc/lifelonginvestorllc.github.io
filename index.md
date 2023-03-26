---
layout: article
title: Investing Journey (投资之旅)
key: page-home
aside:
  toc: true
---

## Investment Performance (投资表现)

**A live trading account with a daily updated chart is worth a thousand words!**

```chart
{
  "type": "line",
  "data": {
    "labels": ["0", "10", "20", "25", "30", "35", "40", "45", "50", "60", "70", "80+"],
    "datasets": [
      {
        "label": "第一曲线（主动收入）",
        "lineTension": 0.3,
        "borderColor": "blue",
        "pointRadius": 0,
        "data": ["NaN", 1, 10, 20, 30, 40, 45, 50, 55, 60, 5, 0]
      },
      {
        "label": "第二曲线（被动收入）",
        "lineTension": 0.3,
        "borderColor": "gold",
        "pointRadius": 0,
        "data": ["NaN", "NaN", 1, 3, 6, 13, 30, 45, 60, 100, 140, 200]
      }      
    ]
  },
  "options": {
    "responsive": true,
    "aspectRatio": 3,
    "layout": {
      "padding": 0
    },    
    "title": {
      "display": true,
      "text": "投资孕育人生财富的第二曲线"
    },
    "legend": {
      "display": true,
      "position": "top"
    }
  }  
}
```