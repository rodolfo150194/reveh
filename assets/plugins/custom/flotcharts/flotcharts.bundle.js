"use strict";

function _typeof(e) {
    return (_typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (e) {
        return typeof e
    } : function (e) {
        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
    })(e)
}

function _typeof(e) {
    return (_typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (e) {
        return typeof e
    } : function (e) {
        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
    })(e)
}

!function (e) {
    var t = function (t, i) {
        var n = i.getElementsByClassName(t)[0];
        if (!n && ((n = document.createElement("canvas")).className = t, n.style.direction = "ltr", n.style.position = "absolute", n.style.left = "0px", n.style.top = "0px", i.appendChild(n), !n.getContext)) throw new Error("Canvas is not available.");
        this.element = n;
        var o = this.context = n.getContext("2d");
        this.pixelRatio = e.plot.browser.getPixelRatio(o);
        var a = e(i).width(), r = e(i).height();
        this.resize(a, r), this.SVGContainer = null, this.SVG = {}, this._textCache = {}
    };

    function i(e, t) {
        e.transform.baseVal.clear(), t && t.forEach((function (t) {
            e.transform.baseVal.appendItem(t)
        }))
    }

    t.prototype.resize = function (e, t) {
        e = e < 10 ? 10 : e, t = t < 10 ? 10 : t;
        var i = this.element, n = this.context, o = this.pixelRatio;
        this.width !== e && (i.width = e * o, i.style.width = e + "px", this.width = e), this.height !== t && (i.height = t * o, i.style.height = t + "px", this.height = t), n.restore(), n.save(), n.scale(o, o)
    }, t.prototype.clear = function () {
        this.context.clearRect(0, 0, this.width, this.height)
    }, t.prototype.render = function () {
        var e = this._textCache;
        for (var t in e) if (hasOwnProperty.call(e, t)) {
            var i = this.getSVGLayer(t), n = e[t], o = i.style.display;
            for (var a in i.style.display = "none", n) if (hasOwnProperty.call(n, a)) {
                var r = n[a];
                for (var s in r) if (hasOwnProperty.call(r, s)) {
                    for (var l, c = r[s], u = c.positions, h = 0; u[h]; h++) if ((l = u[h]).active) l.rendered || (i.appendChild(l.element), l.rendered = !0); else if (u.splice(h--, 1), l.rendered) {
                        for (; l.element.firstChild;) l.element.removeChild(l.element.firstChild);
                        l.element.parentNode.removeChild(l.element)
                    }
                    0 === u.length && (c.measured ? c.measured = !1 : delete r[s])
                }
            }
            i.style.display = o
        }
    }, t.prototype.getSVGLayer = function (e) {
        var t, i = this.SVG[e];
        return i || (this.SVGContainer ? t = this.SVGContainer.firstChild : (this.SVGContainer = document.createElement("div"), this.SVGContainer.className = "flot-svg", this.SVGContainer.style.position = "absolute", this.SVGContainer.style.top = "0px", this.SVGContainer.style.left = "0px", this.SVGContainer.style.height = "100%", this.SVGContainer.style.width = "100%", this.SVGContainer.style.pointerEvents = "none", this.element.parentNode.appendChild(this.SVGContainer), (t = document.createElementNS("http://www.w3.org/2000/svg", "svg")).style.width = "100%", t.style.height = "100%", this.SVGContainer.appendChild(t)), (i = document.createElementNS("http://www.w3.org/2000/svg", "g")).setAttribute("class", e), i.style.position = "absolute", i.style.top = "0px", i.style.left = "0px", i.style.bottom = "0px", i.style.right = "0px", t.appendChild(i), this.SVG[e] = i), i
    }, t.prototype.getTextInfo = function (e, t, i, o, a) {
        var r, s, l, c;
        t = "" + t, r = "object" === _typeof(i) ? i.style + " " + i.variant + " " + i.weight + " " + i.size + "px/" + i.lineHeight + "px " + i.family : i, null == (s = this._textCache[e]) && (s = this._textCache[e] = {}), null == (l = s[r]) && (l = s[r] = {});
        var u = t.replace(/0|1|2|3|4|5|6|7|8|9/g, "0");
        if (!(c = l[u])) {
            var h = document.createElementNS("http://www.w3.org/2000/svg", "text");
            if (-1 !== t.indexOf("<br>")) n(t, h, -9999); else {
                var p = document.createTextNode(t);
                h.appendChild(p)
            }
            h.style.position = "absolute", h.style.maxWidth = a, h.setAttributeNS(null, "x", -9999), h.setAttributeNS(null, "y", -9999), "object" === _typeof(i) ? (h.style.font = r, h.style.fill = i.fill) : "string" == typeof i && h.setAttribute("class", i), this.getSVGLayer(e).appendChild(h);
            var d = h.getBBox();
            for (c = l[u] = {
                width: d.width,
                height: d.height,
                measured: !0,
                element: h,
                positions: []
            }; h.firstChild;) h.removeChild(h.firstChild);
            h.parentNode.removeChild(h)
        }
        return c.measured = !0, c
    }, t.prototype.addText = function (e, t, o, a, r, s, l, c, u, h) {
        var p = this.getTextInfo(e, a, r, s, l), d = p.positions;
        "center" === c ? t -= p.width / 2 : "right" === c && (t -= p.width), "middle" === u ? o -= p.height / 2 : "bottom" === u && (o -= p.height), o += .75 * p.height;
        for (var f, g = 0; d[g]; g++) {
            if ((f = d[g]).x === t && f.y === o && f.text === a) return f.active = !0, void i(f.element, h);
            if (!1 === f.active) return f.active = !0, -1 !== (f.text = a).indexOf("<br>") ? (o -= .25 * p.height, n(a, f.element, t)) : f.element.textContent = a, f.element.setAttributeNS(null, "x", t), f.element.setAttributeNS(null, "y", o), f.x = t, f.y = o, void i(f.element, h)
        }
        f = {
            active: !0,
            rendered: !1,
            element: d.length ? p.element.cloneNode() : p.element,
            text: a,
            x: t,
            y: o
        }, d.push(f), -1 !== a.indexOf("<br>") ? (o -= .25 * p.height, n(a, f.element, t)) : f.element.textContent = a, f.element.setAttributeNS(null, "x", t), f.element.setAttributeNS(null, "y", o), f.element.style.textAlign = c, i(f.element, h)
    };
    var n = function (e, t, i) {
        var n, o, a, r = e.split("<br>");
        for (o = 0; o < r.length; o++) t.childNodes[o] ? n = t.childNodes[o] : (n = document.createElementNS("http://www.w3.org/2000/svg", "tspan"), t.appendChild(n)), n.textContent = r[o], a = (0 === o ? 0 : 1) + "em", n.setAttributeNS(null, "dy", a), n.setAttributeNS(null, "x", i)
    };
    t.prototype.removeText = function (e, t, i, n, o, a) {
        var r, s;
        if (null == n) {
            var l = this._textCache[e];
            if (null != l) for (var c in l) if (hasOwnProperty.call(l, c)) {
                var u = l[c];
                for (var h in u) if (hasOwnProperty.call(u, h)) {
                    var p = u[h].positions;
                    p.forEach((function (e) {
                        e.active = !1
                    }))
                }
            }
        } else (p = (r = this.getTextInfo(e, n, o, a)).positions).forEach((function (e) {
            s = i + .75 * r.height, e.x === t && e.y === s && e.text === n && (e.active = !1)
        }))
    }, t.prototype.clearCache = function () {
        var e = this._textCache;
        for (var t in e) if (hasOwnProperty.call(e, t)) for (var i = this.getSVGLayer(t); i.firstChild;) i.removeChild(i.firstChild);
        this._textCache = {}
    }, window.Flot || (window.Flot = {}), window.Flot.Canvas = t
}(jQuery), function (e) {
    e.color = {}, e.color.make = function (t, i, n, o) {
        var a = {};
        return a.r = t || 0, a.g = i || 0, a.b = n || 0, a.a = null != o ? o : 1, a.add = function (e, t) {
            for (var i = 0; i < e.length; ++i) a[e.charAt(i)] += t;
            return a.normalize()
        }, a.scale = function (e, t) {
            for (var i = 0; i < e.length; ++i) a[e.charAt(i)] *= t;
            return a.normalize()
        }, a.toString = function () {
            return 1 <= a.a ? "rgb(" + [a.r, a.g, a.b].join(",") + ")" : "rgba(" + [a.r, a.g, a.b, a.a].join(",") + ")"
        }, a.normalize = function () {
            function e(e, t, i) {
                return t < e ? e : i < t ? i : t
            }

            return a.r = e(0, parseInt(a.r), 255), a.g = e(0, parseInt(a.g), 255), a.b = e(0, parseInt(a.b), 255), a.a = e(0, a.a, 1), a
        }, a.clone = function () {
            return e.color.make(a.r, a.b, a.g, a.a)
        }, a.normalize()
    }, e.color.extract = function (t, i) {
        var n;
        do {
            if ("" !== (n = t.css(i).toLowerCase()) && "transparent" !== n) break;
            t = t.parent()
        } while (t.length && !e.nodeName(t.get(0), "body"));
        return "rgba(0, 0, 0, 0)" === n && (n = "transparent"), e.color.parse(n)
    }, e.color.parse = function (i) {
        var n, o = e.color.make;
        if (n = /rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(i)) return o(parseInt(n[1], 10), parseInt(n[2], 10), parseInt(n[3], 10));
        if (n = /rgba\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)/.exec(i)) return o(parseInt(n[1], 10), parseInt(n[2], 10), parseInt(n[3], 10), parseFloat(n[4]));
        if (n = /rgb\(\s*([0-9]+(?:\.[0-9]+)?)%\s*,\s*([0-9]+(?:\.[0-9]+)?)%\s*,\s*([0-9]+(?:\.[0-9]+)?)%\s*\)/.exec(i)) return o(2.55 * parseFloat(n[1]), 2.55 * parseFloat(n[2]), 2.55 * parseFloat(n[3]));
        if (n = /rgba\(\s*([0-9]+(?:\.[0-9]+)?)%\s*,\s*([0-9]+(?:\.[0-9]+)?)%\s*,\s*([0-9]+(?:\.[0-9]+)?)%\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)/.exec(i)) return o(2.55 * parseFloat(n[1]), 2.55 * parseFloat(n[2]), 2.55 * parseFloat(n[3]), parseFloat(n[4]));
        if (n = /#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(i)) return o(parseInt(n[1], 16), parseInt(n[2], 16), parseInt(n[3], 16));
        if (n = /#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(i)) return o(parseInt(n[1] + n[1], 16), parseInt(n[2] + n[2], 16), parseInt(n[3] + n[3], 16));
        var a = e.trim(i).toLowerCase();
        return "transparent" === a ? o(255, 255, 255, 0) : o((n = t[a] || [0, 0, 0])[0], n[1], n[2])
    };
    var t = {
        aqua: [0, 255, 255],
        azure: [240, 255, 255],
        beige: [245, 245, 220],
        black: [0, 0, 0],
        blue: [0, 0, 255],
        brown: [165, 42, 42],
        cyan: [0, 255, 255],
        darkblue: [0, 0, 139],
        darkcyan: [0, 139, 139],
        darkgrey: [169, 169, 169],
        darkgreen: [0, 100, 0],
        darkkhaki: [189, 183, 107],
        darkmagenta: [139, 0, 139],
        darkolivegreen: [85, 107, 47],
        darkorange: [255, 140, 0],
        darkorchid: [153, 50, 204],
        darkred: [139, 0, 0],
        darksalmon: [233, 150, 122],
        darkviolet: [148, 0, 211],
        fuchsia: [255, 0, 255],
        gold: [255, 215, 0],
        green: [0, 128, 0],
        indigo: [75, 0, 130],
        khaki: [240, 230, 140],
        lightblue: [173, 216, 230],
        lightcyan: [224, 255, 255],
        lightgreen: [144, 238, 144],
        lightgrey: [211, 211, 211],
        lightpink: [255, 182, 193],
        lightyellow: [255, 255, 224],
        lime: [0, 255, 0],
        magenta: [255, 0, 255],
        maroon: [128, 0, 0],
        navy: [0, 0, 128],
        olive: [128, 128, 0],
        orange: [255, 165, 0],
        pink: [255, 192, 203],
        purple: [128, 0, 128],
        violet: [128, 0, 128],
        red: [255, 0, 0],
        silver: [192, 192, 192],
        white: [255, 255, 255],
        yellow: [255, 255, 0]
    }
}(jQuery), function (e) {
    var t = window.Flot.Canvas;

    function i(t) {
        var i, n = [], o = e.plot.saturated.saturate(e.plot.saturated.floorInBase(t.min, t.tickSize)), a = 0,
            r = Number.NaN;
        for (o === -Number.MAX_VALUE && (n.push(o), o = e.plot.saturated.floorInBase(t.min + t.tickSize, t.tickSize)); i = r, r = e.plot.saturated.multiplyAdd(t.tickSize, a, o), n.push(r), ++a, r < t.max && r !== i;) ;
        return n
    }

    function n(e, t, i) {
        var n = t.tickDecimals;
        if (-1 !== ("" + e).indexOf("e")) return o(e, t, i);
        0 < i && (t.tickDecimals = i);
        var a = t.tickDecimals ? parseFloat("1e" + t.tickDecimals) : 1, r = "" + Math.round(e * a) / a;
        if (null != t.tickDecimals) {
            var s = r.indexOf("."), l = -1 === s ? 0 : r.length - s - 1;
            l < t.tickDecimals && (r = (l ? r : r + ".") + ("" + a).substr(1, t.tickDecimals - l))
        }
        return t.tickDecimals = n, r
    }

    function o(e, t, i) {
        var n = ("" + e).indexOf("e"), o = parseInt(("" + e).substr(n + 1)),
            r = -1 !== n ? o : 0 < e ? Math.floor(Math.log(e) / Math.LN10) : 0, s = parseFloat("1e" + r), l = e / s;
        if (i) {
            var c = a(e, i);
            return (e / s).toFixed(c) + "e" + r
        }
        return 0 < t.tickDecimals ? l.toFixed(a(e, t.tickDecimals)) + "e" + r : l.toFixed() + "e" + r
    }

    function a(e, t) {
        var i = Math.log(Math.abs(e)) * Math.LOG10E, n = Math.abs(i + t);
        return n <= 20 ? Math.floor(n) : 20
    }

    function r(o, a, r, s) {
        var l = [], c = {
                colors: ["#edc240", "#afd8f8", "#cb4b4b", "#4da74d", "#9440ed"],
                xaxis: {
                    show: null,
                    position: "bottom",
                    mode: null,
                    font: null,
                    color: null,
                    tickColor: null,
                    transform: null,
                    inverseTransform: null,
                    min: null,
                    max: null,
                    autoScaleMargin: null,
                    autoScale: "exact",
                    windowSize: null,
                    growOnly: null,
                    ticks: null,
                    tickFormatter: null,
                    showTickLabels: "major",
                    labelWidth: null,
                    labelHeight: null,
                    reserveSpace: null,
                    tickLength: null,
                    showMinorTicks: null,
                    showTicks: null,
                    gridLines: null,
                    alignTicksWithAxis: null,
                    tickDecimals: null,
                    tickSize: null,
                    minTickSize: null,
                    offset: {below: 0, above: 0},
                    boxPosition: {centerX: 0, centerY: 0}
                },
                yaxis: {
                    autoScaleMargin: .02,
                    autoScale: "loose",
                    growOnly: null,
                    position: "left",
                    showTickLabels: "major",
                    offset: {below: 0, above: 0},
                    boxPosition: {centerX: 0, centerY: 0}
                },
                xaxes: [],
                yaxes: [],
                series: {
                    points: {show: !1, radius: 3, lineWidth: 2, fill: !0, fillColor: "#ffffff", symbol: "circle"},
                    lines: {lineWidth: 1, fill: !1, fillColor: null, steps: !1},
                    bars: {
                        show: !1,
                        lineWidth: 2,
                        horizontal: !1,
                        barWidth: .8,
                        fill: !0,
                        fillColor: null,
                        align: "left",
                        zero: !0
                    },
                    shadowSize: 3,
                    highlightColor: null
                },
                grid: {
                    show: !0,
                    aboveData: !1,
                    color: "#545454",
                    backgroundColor: null,
                    borderColor: null,
                    tickColor: null,
                    margin: 0,
                    labelMargin: 5,
                    axisMargin: 8,
                    borderWidth: 1,
                    minBorderMargin: null,
                    markings: null,
                    markingsColor: "#f4f4f4",
                    markingsLineWidth: 2,
                    clickable: !1,
                    hoverable: !1,
                    autoHighlight: !0,
                    mouseActiveRadius: 15
                },
                interaction: {redrawOverlayInterval: 1e3 / 60},
                hooks: {}
            }, u = null, h = null, p = null, d = null, f = null, g = [], m = [], v = {left: 0, right: 0, top: 0, bottom: 0},
            x = 0, b = 0, y = {
                processOptions: [],
                processRawData: [],
                processDatapoints: [],
                processOffset: [],
                setupGrid: [],
                adjustSeriesDataRange: [],
                setRange: [],
                drawBackground: [],
                drawSeries: [],
                drawAxis: [],
                draw: [],
                findNearbyItems: [],
                axisReserveSpace: [],
                bindEvents: [],
                drawOverlay: [],
                resize: [],
                shutdown: []
            }, w = this, k = {}, T = null;
        w.setData = C, w.setupGrid = R, w.draw = G, w.getPlaceholder = function () {
            return o
        }, w.getCanvas = function () {
            return u.element
        }, w.getSurface = function () {
            return u
        }, w.getEventHolder = function () {
            return p[0]
        }, w.getPlotOffset = function () {
            return v
        }, w.width = function () {
            return x
        }, w.height = function () {
            return b
        }, w.offset = function () {
            var e = p.offset();
            return e.left += v.left, e.top += v.top, e
        }, w.getData = function () {
            return l
        }, w.getAxes = function () {
            var t = {};
            return e.each(g.concat(m), (function (e, i) {
                i && (t[i.direction + (1 !== i.n ? i.n : "") + "axis"] = i)
            })), t
        }, w.getXAxes = function () {
            return g
        }, w.getYAxes = function () {
            return m
        }, w.c2p = function (e) {
            var t, i, n = {};
            for (t = 0; t < g.length; ++t) (i = g[t]) && i.used && (n["x" + i.n] = i.c2p(e.left));
            for (t = 0; t < m.length; ++t) (i = m[t]) && i.used && (n["y" + i.n] = i.c2p(e.top));
            return void 0 !== n.x1 && (n.x = n.x1), void 0 !== n.y1 && (n.y = n.y1), n
        }, w.p2c = function (e) {
            var t, i, n, o = {};
            for (t = 0; t < g.length; ++t) if ((i = g[t]) && i.used && (null == e[n = "x" + i.n] && 1 === i.n && (n = "x"), null != e[n])) {
                o.left = i.p2c(e[n]);
                break
            }
            for (t = 0; t < m.length; ++t) if ((i = m[t]) && i.used && (null == e[n = "y" + i.n] && 1 === i.n && (n = "y"), null != e[n])) {
                o.top = i.p2c(e[n]);
                break
            }
            return o
        }, w.getOptions = function () {
            return c
        }, w.triggerRedrawOverlay = $, w.pointOffset = function (e) {
            return {
                left: parseInt(g[A(e, "x") - 1].p2c(+e.x) + v.left, 10),
                top: parseInt(m[A(e, "y") - 1].p2c(+e.y) + v.top, 10)
            }
        }, w.shutdown = N, w.destroy = function () {
            N(), o.removeData("plot").empty(), l = [], g = [], m = [], w = y = f = d = p = h = u = c = null
        }, w.resize = function () {
            var e = o.width(), t = o.height();
            u.resize(e, t), h.resize(e, t), P(y.resize, [e, t])
        }, w.clearTextCache = function () {
            u.clearCache(), h.clearCache()
        }, w.autoScaleAxis = F, w.computeRangeForDataSeries = function (e, t, i) {
            for (var n = e.datapoints.points, o = e.datapoints.pointsize, a = e.datapoints.format, r = Number.POSITIVE_INFINITY, s = Number.NEGATIVE_INFINITY, l = {
                xmin: r,
                ymin: r,
                xmax: s,
                ymax: s
            }, c = 0; c < n.length; c += o) if (null !== n[c] && ("function" != typeof i || i(n[c]))) for (var u = 0; u < o; ++u) {
                var h = n[c + u], p = a[u];
                null != p && ("function" != typeof i || i(h)) && (t || p.computeRange) && h !== 1 / 0 && h !== -1 / 0 && (!0 === p.x && (h < l.xmin && (l.xmin = h), h > l.xmax && (l.xmax = h)), !0 === p.y && (h < l.ymin && (l.ymin = h), h > l.ymax && (l.ymax = h)))
            }
            return l
        }, w.adjustSeriesDataRange = function (e, t) {
            if (e.bars.show) {
                var i, n = e.bars.barWidth[1];
                e.datapoints && e.datapoints.points && !n && function (e) {
                    var t = [], i = e.datapoints.pointsize, n = Number.MAX_VALUE;
                    e.datapoints.points.length <= i && (n = 1);
                    for (var o = e.bars.horizontal ? 1 : 0; o < e.datapoints.points.length; o += i) isFinite(e.datapoints.points[o]) && null !== e.datapoints.points[o] && t.push(e.datapoints.points[o]);
                    (t = t.filter((function (e, t, i) {
                        return i.indexOf(e) === t
                    }))).sort((function (e, t) {
                        return e - t
                    }));
                    for (var a = 1; a < t.length; a++) {
                        var r = Math.abs(t[a] - t[a - 1]);
                        r < n && isFinite(r) && (n = r)
                    }
                    "number" == typeof e.bars.barWidth ? e.bars.barWidth = e.bars.barWidth * n : e.bars.barWidth[0] = e.bars.barWidth[0] * n
                }(e);
                var o = e.bars.barWidth[0] || e.bars.barWidth;
                switch (e.bars.align) {
                    case"left":
                        i = 0;
                        break;
                    case"right":
                        i = -o;
                        break;
                    default:
                        i = -o / 2
                }
                e.bars.horizontal ? (t.ymin += i, t.ymax += i + o) : (t.xmin += i, t.xmax += i + o)
            }
            (e.bars.show && e.bars.zero || e.lines.show && e.lines.zero) && (e.datapoints.pointsize <= 2 && (t.ymin = Math.min(0, t.ymin), t.ymax = Math.max(0, t.ymax)));
            return t
        }, w.findNearbyItem = function (e, t, i, n, o) {
            var a = Z(e, t, i, n, o);
            return void 0 !== a[0] ? a[0] : null
        }, w.findNearbyItems = Z, w.findNearbyInterpolationPoint = function (e, t, i) {
            var n, o, a, r, s, c, u, h = Number.MAX_VALUE;
            for (n = 0; n < l.length; ++n) if (i(n)) {
                var p = l[n].datapoints.points;
                c = l[n].datapoints.pointsize;
                var d = p[p.length - c] < p[0] ? function (e, t) {
                    return t < e
                } : function (e, t) {
                    return e < t
                };
                if (!d(e, p[0])) {
                    for (o = c; o < p.length && !d(e, p[o]); o += c) ;
                    var f = p[o - c], g = p[o - c + 1], m = p[o], v = p[o + 1];
                    void 0 !== f && void 0 !== m && void 0 !== g && void 0 !== v && (t = f === m ? v : g + (v - g) * (e - f) / (m - f), (a = (r = Math.abs(l[n].xaxis.p2c(m) - e)) * r + (s = Math.abs(l[n].yaxis.p2c(v) - t)) * s) < h && (h = a, u = [e, t, n, o]))
                }
            }
            return u ? (n = u[2], o = u[3], c = l[n].datapoints.pointsize, f = (p = l[n].datapoints.points)[o - c], g = p[o - c + 1], m = p[o], v = p[o + 1], {
                datapoint: [u[0], u[1]],
                leftPoint: [f, g],
                rightPoint: [m, v],
                seriesIndex: n
            }) : null
        }, w.computeValuePrecision = D, w.computeTickSize = W, w.addEventHandler = function (e, t, i, n) {
            var o = i + e, a = k[o] || [];
            a.push({event: e, handler: t, eventHolder: i, priority: n}), a.sort((function (e, t) {
                return t.priority - e.priority
            })), a.forEach((function (e) {
                e.eventHolder.unbind(e.event, e.handler), e.eventHolder.bind(e.event, e.handler)
            })), k[o] = a
        }, w.hooks = y;
        var M = e.plot.uiConstants.MINOR_TICKS_COUNT_CONSTANT, S = e.plot.uiConstants.TICK_LENGTH_CONSTANT;

        function P(e, t) {
            t = [w].concat(t);
            for (var i = 0; i < e.length; ++i) e[i].apply(this, t)
        }

        function C(t) {
            var i = l;
            l = function (t) {
                for (var i = [], n = 0; n < t.length; ++n) {
                    var o = e.extend(!0, {}, c.series);
                    null != t[n].data ? (o.data = t[n].data, delete t[n].data, e.extend(!0, o, t[n]), t[n].data = o.data) : o.data = t[n], i.push(o)
                }
                return i
            }(t), function () {
                var t, i = l.length, n = -1;
                for (t = 0; t < l.length; ++t) {
                    var o = l[t].color;
                    null != o && (i--, "number" == typeof o && n < o && (n = o))
                }
                i <= n && (i = n + 1);
                var a, r = [], s = c.colors, u = s.length, h = 0, p = Math.max(0, l.length - i);
                for (t = 0; t < i; t++) a = e.color.parse(s[(p + t) % u] || "#666"), t % u == 0 && t && (h = 0 <= h ? h < .5 ? -h - .2 : 0 : -h), r[t] = a.scale("rgb", 1 + h);
                var d, f = 0;
                for (t = 0; t < l.length; ++t) {
                    if (null == (d = l[t]).color ? (d.color = r[f].toString(), ++f) : "number" == typeof d.color && (d.color = r[d.color].toString()), null == d.lines.show) {
                        var v, x = !0;
                        for (v in d) if (d[v] && d[v].show) {
                            x = !1;
                            break
                        }
                        x && (d.lines.show = !0)
                    }
                    null == d.lines.zero && (d.lines.zero = !!d.lines.fill), d.xaxis = z(g, A(d, "x")), d.yaxis = z(m, A(d, "y"))
                }
            }(), function (t) {
                var i, n, o, a, r, s, c, u, h, p, d, f, g = Number.POSITIVE_INFINITY, m = Number.NEGATIVE_INFINITY;

                function v(e, t, i) {
                    t < e.datamin && t !== -1 / 0 && (e.datamin = t), i > e.datamax && i !== 1 / 0 && (e.datamax = i)
                }

                function x(e, t) {
                    return e && e[t] && e[t].datapoints && e[t].datapoints.points ? e[t].datapoints.points : []
                }

                for (e.each(L(), (function (e, t) {
                    !0 !== t.options.growOnly ? (t.datamin = g, t.datamax = m) : (void 0 === t.datamin && (t.datamin = g), void 0 === t.datamax && (t.datamax = m)), t.used = !1
                })), i = 0; i < l.length; ++i) (r = l[i]).datapoints = {points: []}, 0 === r.datapoints.points.length && (r.datapoints.points = x(t, i)), P(y.processRawData, [r, r.data, r.datapoints]);
                for (i = 0; i < l.length; ++i) {
                    if (d = (r = l[i]).data, !(f = r.datapoints.format)) {
                        if ((f = []).push({
                            x: !0,
                            y: !1,
                            number: !0,
                            required: !0,
                            computeRange: "none" !== r.xaxis.options.autoScale,
                            defaultValue: null
                        }), f.push({
                            x: !1,
                            y: !0,
                            number: !0,
                            required: !0,
                            computeRange: "none" !== r.yaxis.options.autoScale,
                            defaultValue: null
                        }), r.stack || r.bars.show || r.lines.show && r.lines.fill) 2 < (null != r.datapoints.pointsize ? r.datapoints.pointsize : r.data && r.data[0] && r.data[0].length ? r.data[0].length : 3) && f.push({
                            x: r.bars.horizontal,
                            y: !r.bars.horizontal,
                            number: !0,
                            required: !1,
                            computeRange: "none" !== r.yaxis.options.autoScale,
                            defaultValue: 0
                        });
                        r.datapoints.format = f
                    }
                    if (r.xaxis.used = r.yaxis.used = !0, null == r.datapoints.pointsize) {
                        for (r.datapoints.pointsize = f.length, c = r.datapoints.pointsize, s = r.datapoints.points, n = o = 0; n < d.length; ++n, o += c) {
                            var b = null == (p = d[n]);
                            if (!b) for (a = 0; a < c; ++a) u = p[a], (h = f[a]) && (h.number && null != u && (u = +u, isNaN(u) && (u = null)), null == u && (h.required && (b = !0), null != h.defaultValue && (u = h.defaultValue))), s[o + a] = u;
                            if (b) for (a = 0; a < c; ++a) null != (u = s[o + a]) && (h = f[a]).computeRange && (h.x && v(r.xaxis, u, u), h.y && v(r.yaxis, u, u)), s[o + a] = null
                        }
                        s.length = o
                    }
                }
                for (i = 0; i < l.length; ++i) r = l[i], P(y.processDatapoints, [r, r.datapoints]);
                for (i = 0; i < l.length; ++i) if (!(f = (r = l[i]).datapoints.format).every((function (e) {
                    return !e.computeRange
                }))) {
                    var k = w.adjustSeriesDataRange(r, w.computeRangeForDataSeries(r));
                    P(y.adjustSeriesDataRange, [r, k]), v(r.xaxis, k.xmin, k.xmax), v(r.yaxis, k.ymin, k.ymax)
                }
                e.each(L(), (function (e, t) {
                    t.datamin === g && (t.datamin = null), t.datamax === m && (t.datamax = null)
                }))
            }(i)
        }

        function A(e, t) {
            var i = e[t + "axis"];
            return "object" === _typeof(i) && (i = i.n), "number" != typeof i && (i = 1), i
        }

        function L() {
            return g.concat(m).filter((function (e) {
                return e
            }))
        }

        function z(t, i) {
            return t[i - 1] || (t[i - 1] = {
                n: i,
                direction: t === g ? "x" : "y",
                options: e.extend(!0, {}, t === g ? c.xaxis : c.yaxis)
            }), t[i - 1]
        }

        function N() {
            T && clearTimeout(T), P(y.shutdown, [p])
        }

        function O(t) {
            function i(e) {
                return e
            }

            var n, o, a = t.options.transform || i, r = t.options.inverseTransform;
            o = "x" === t.direction ? (n = isFinite(a(t.max) - a(t.min)) ? t.scale = x / Math.abs(a(t.max) - a(t.min)) : t.scale = 1 / Math.abs(e.plot.saturated.delta(a(t.min), a(t.max), x)), Math.min(a(t.max), a(t.min))) : (n = -(n = isFinite(a(t.max) - a(t.min)) ? t.scale = b / Math.abs(a(t.max) - a(t.min)) : t.scale = 1 / Math.abs(e.plot.saturated.delta(a(t.min), a(t.max), b))), Math.max(a(t.max), a(t.min))), t.p2c = a === i ? function (e) {
                return isFinite(e - o) ? (e - o) * n : (e / 4 - o / 4) * n * 4
            } : function (e) {
                var t = a(e);
                return isFinite(t - o) ? (t - o) * n : (t / 4 - o / 4) * n * 4
            }, t.c2p = r ? function (e) {
                return r(o + e / n)
            } : function (e) {
                return o + e / n
            }
        }

        function I(t) {
            P(y.axisReserveSpace, [t]);
            var i = t.labelWidth, n = t.labelHeight, o = t.options.position, a = "x" === t.direction,
                r = t.options.tickLength, s = t.options.showTicks, l = t.options.showMinorTicks,
                h = t.options.gridLines, p = c.grid.axisMargin, d = c.grid.labelMargin, f = !0, x = !0, b = !1;
            e.each(a ? g : m, (function (e, i) {
                i && (i.show || i.reserveSpace) && (i === t ? b = !0 : i.options.position === o && (b ? x = !1 : f = !1))
            })), x && (p = 0), null == r && (r = S), null == s && (s = !0), null == l && (l = !0), null == h && (h = !!f), isNaN(+r) || (d += s ? +r : 0), a ? (n += d, "bottom" === o ? (v.bottom += n + p, t.box = {
                top: u.height - v.bottom,
                height: n
            }) : (t.box = {
                top: v.top + p,
                height: n
            }, v.top += n + p)) : (i += d, "left" === o ? (t.box = {
                left: v.left + p,
                width: i
            }, v.left += i + p) : (v.right += i + p, t.box = {
                left: u.width - v.right,
                width: i
            })), t.position = o, t.tickLength = r, t.showMinorTicks = l, t.showTicks = s, t.gridLines = h, t.box.padding = d, t.innermost = f
        }

        function E(e, t, i) {
            "x" === e.direction ? ("bottom" === e.position && i(t.bottom) && (e.box.top -= Math.ceil(t.bottom)), "top" === e.position && i(t.top) && (e.box.top += Math.ceil(t.top))) : ("left" === e.position && i(t.left) && (e.box.left += Math.ceil(t.left)), "right" === e.position && i(t.right) && (e.box.left -= Math.ceil(t.right)))
        }

        function R(t) {
            var o, a, r = L(), s = c.grid.show;
            for (a in v) v[a] = 0;
            for (a in P(y.processOffset, [v]), v) "object" === _typeof(c.grid.borderWidth) ? v[a] += s ? c.grid.borderWidth[a] : 0 : v[a] += s ? c.grid.borderWidth : 0;
            if (e.each(r, (function (i, o) {
                var a, r, s = o.options;
                o.show = null == s.show ? o.used : s.show, o.reserveSpace = null == s.reserveSpace ? o.show : s.reserveSpace, r = (a = o).options, a.tickFormatter || ("function" == typeof r.tickFormatter ? a.tickFormatter = function () {
                    var e = Array.prototype.slice.call(arguments);
                    return "" + r.tickFormatter.apply(null, e)
                } : a.tickFormatter = n), P(y.setRange, [o, t]), function (t, i) {
                    var n = "number" == typeof t.options.min ? t.options.min : t.min,
                        o = "number" == typeof t.options.max ? t.options.max : t.max, a = t.options.offset;
                    if (i && (F(t), n = t.autoScaledMin, o = t.autoScaledMax), n = (null != n ? n : -1) + (a.below || 0), (o = (null != o ? o : 1) + (a.above || 0)) < n) {
                        var r = n;
                        n = o, o = r, t.options.offset = {above: 0, below: 0}
                    }
                    t.min = e.plot.saturated.saturate(n), t.max = e.plot.saturated.saturate(o)
                }(o, t)
            })), s) {
                x = u.width - v.left - v.right, b = u.height - v.bottom - v.top;
                var h = e.grep(r, (function (e) {
                    return e.show || e.reserveSpace
                }));
                for (e.each(h, (function (t, n) {
                    var o, a, r, s;
                    !function (t) {
                        var n, o = t.options;
                        n = Y(t.direction, u, o.ticks), t.delta = e.plot.saturated.delta(t.min, t.max, n);
                        var a = w.computeValuePrecision(t.min, t.max, t.direction, n, o.tickDecimals);
                        if (t.tickDecimals = Math.max(0, null != o.tickDecimals ? o.tickDecimals : a), t.tickSize = function (e, t, i, n, o) {
                            var a = W(e, t, "number" == typeof n.ticks && 0 < n.ticks ? n.ticks : .3 * Math.sqrt("x" === i ? u.width : u.height), o);
                            return null != n.minTickSize && a < n.minTickSize && (a = n.minTickSize), n.tickSize || a
                        }(t.min, t.max, t.direction, o, o.tickDecimals), t.tickGenerator || ("function" == typeof o.tickGenerator ? t.tickGenerator = o.tickGenerator : t.tickGenerator = i), null != o.alignTicksWithAxis) {
                            var r = ("x" === t.direction ? g : m)[o.alignTicksWithAxis - 1];
                            if (r && r.used && r !== t) {
                                var s = t.tickGenerator(t, w);
                                if (0 < s.length && (null == o.min && (t.min = Math.min(t.min, s[0])), null == o.max && 1 < s.length && (t.max = Math.max(t.max, s[s.length - 1]))), t.tickGenerator = function (e) {
                                    var t, i, n = [];
                                    for (i = 0; i < r.ticks.length; ++i) t = (r.ticks[i].v - r.min) / (r.max - r.min), t = e.min + t * (e.max - e.min), n.push(t);
                                    return n
                                }, !t.mode && null == o.tickDecimals) {
                                    var l = Math.max(0, 1 - Math.floor(Math.log(t.delta) / Math.LN10)),
                                        c = t.tickGenerator(t, w);
                                    1 < c.length && /\..*0$/.test((c[1] - c[0]).toFixed(l)) || (t.tickDecimals = l)
                                }
                            }
                        }
                    }(n), function (t) {
                        var i, n, o = t.options.ticks, a = [];
                        for (null == o || "number" == typeof o && 0 < o ? a = t.tickGenerator(t, w) : o && (a = e.isFunction(o) ? o(t) : o), t.ticks = [], i = 0; i < a.length; ++i) {
                            var r = null, s = a[i];
                            "object" === _typeof(s) ? (n = +s[0], 1 < s.length && (r = s[1])) : n = +s, isNaN(n) || t.ticks.push(X(n, r, t, "major"))
                        }
                    }(n), a = (o = n).ticks, r = l, "loose" === o.options.autoScale && 0 < a.length && r.some((function (e) {
                        return 0 < e.datapoints.points.length
                    })) && (o.min = Math.min(o.min, a[0].v), o.max = Math.max(o.max, a[a.length - 1].v)), O(n), function (e, t) {
                        if ("endpoints" === e.options.showTickLabels) return !0;
                        if ("all" !== e.options.showTickLabels) return "major" !== e.options.showTickLabels && "none" !== e.options.showTickLabels && void 0;
                        var i = t.filter((function (t) {
                            return t.bars.horizontal ? t.yaxis === e : t.xaxis === e
                        })), n = i.some((function (e) {
                            return !e.bars.show
                        }));
                        return 0 === i.length || n
                    }(s = n, l) && (s.ticks.unshift(X(s.min, null, s, "min")), s.ticks.push(X(s.max, null, s, "max"))), function (e) {
                        for (var t = e.options, i = "none" !== t.showTickLabels && e.ticks ? e.ticks : [], n = "major" === t.showTickLabels || "all" === t.showTickLabels, o = "endpoints" === t.showTickLabels || "all" === t.showTickLabels, a = t.labelWidth || 0, r = t.labelHeight || 0, s = e.direction + "Axis " + e.direction + e.n + "Axis", l = "flot-" + e.direction + "-axis flot-" + e.direction + e.n + "-axis " + s, c = t.font || "flot-tick-label tickLabel", h = 0; h < i.length; ++h) {
                            var p = i[h], d = p.label;
                            if (p.label && !(!1 === n && 0 < h && h < i.length - 1) && (!1 !== o || 0 !== h && h !== i.length - 1)) {
                                "object" === _typeof(p.label) && (d = p.label.name);
                                var f = u.getTextInfo(l, d, c);
                                a = Math.max(a, f.width), r = Math.max(r, f.height)
                            }
                        }
                        e.labelWidth = t.labelWidth || a, e.labelHeight = t.labelHeight || r
                    }(n)
                })), o = h.length - 1; 0 <= o; --o) I(h[o]);
                !function () {
                    var t, i = c.grid.minBorderMargin;
                    if (null == i) for (t = i = 0; t < l.length; ++t) i = Math.max(i, 2 * (l[t].points.radius + l[t].points.lineWidth / 2));
                    var n, o = {}, a = {left: i, right: i, top: i, bottom: i};
                    for (n in e.each(L(), (function (e, t) {
                        t.reserveSpace && t.ticks && t.ticks.length && ("x" === t.direction ? (a.left = Math.max(a.left, t.labelWidth / 2), a.right = Math.max(a.right, t.labelWidth / 2)) : (a.bottom = Math.max(a.bottom, t.labelHeight / 2), a.top = Math.max(a.top, t.labelHeight / 2)))
                    })), a) o[n] = a[n] - v[n];
                    e.each(g.concat(m), (function (e, t) {
                        E(t, o, (function (e) {
                            return 0 < e
                        }))
                    })), v.left = Math.ceil(Math.max(a.left, v.left)), v.right = Math.ceil(Math.max(a.right, v.right)), v.top = Math.ceil(Math.max(a.top, v.top)), v.bottom = Math.ceil(Math.max(a.bottom, v.bottom))
                }(), e.each(h, (function (e, t) {
                    var i;
                    "x" === (i = t).direction ? (i.box.left = v.left - i.labelWidth / 2, i.box.width = u.width - v.left - v.right + i.labelWidth) : (i.box.top = v.top - i.labelHeight / 2, i.box.height = u.height - v.bottom - v.top + i.labelHeight)
                }))
            }
            if (c.grid.margin) {
                for (a in v) {
                    var p = c.grid.margin || 0;
                    v[a] += "number" == typeof p ? p : p[a] || 0
                }
                e.each(g.concat(m), (function (e, t) {
                    E(t, c.grid.margin, (function (e) {
                        return null != e
                    }))
                }))
            }
            x = u.width - v.left - v.right, b = u.height - v.bottom - v.top, e.each(r, (function (e, t) {
                O(t)
            })), s && e.each(L(), (function (e, t) {
                var i, n, o, a, r, s, l, c = t.box, h = t.direction + "Axis " + t.direction + t.n + "Axis",
                    p = "flot-" + t.direction + "-axis flot-" + t.direction + t.n + "-axis " + h,
                    d = t.options.font || "flot-tick-label tickLabel", f = {x: NaN, y: NaN, width: NaN, height: NaN},
                    g = [], m = function (e, i) {
                        return !e || !e.label || e.v < t.min || e.v > t.max ? f : (s = u.getTextInfo(p, e.label, d), "x" === t.direction ? (a = "center", n = v.left + t.p2c(e.v), "bottom" === t.position ? o = c.top + c.padding - t.boxPosition.centerY : (o = c.top + c.height - c.padding + t.boxPosition.centerY, r = "bottom")) : (r = "middle", o = v.top + t.p2c(e.v), "left" === t.position ? (n = c.left + c.width - c.padding - t.boxPosition.centerX, a = "right") : n = c.left + c.padding + t.boxPosition.centerX), l = {
                            x: n - s.width / 2 - 3,
                            y: o - 3,
                            width: s.width + 6,
                            height: s.height + 6
                        }, h = l, i.some((function (e) {
                            return function (e, t, i, n, o, a, r, s) {
                                return (e <= o && o <= i || o <= e && e <= r) && (t <= a && a <= n || a <= t && t <= s)
                            }(h.x, h.y, h.x + h.width, h.y + h.height, e.x, e.y, e.x + e.width, e.y + e.height)
                        })) ? f : (u.addText(p, n, o, e.label, d, null, null, a, r), l));
                        var h
                    };
                if (u.removeText(p), P(y.drawAxis, [t, u]), t.show) switch (t.options.showTickLabels) {
                    case"none":
                        break;
                    case"endpoints":
                        g.push(m(t.ticks[0], g)), g.push(m(t.ticks[t.ticks.length - 1], g));
                        break;
                    case"major":
                        for (g.push(m(t.ticks[0], g)), g.push(m(t.ticks[t.ticks.length - 1], g)), i = 1; i < t.ticks.length - 1; ++i) g.push(m(t.ticks[i], g));
                        break;
                    case"all":
                        for (g.push(m(t.ticks[0], [])), g.push(m(t.ticks[t.ticks.length - 1], g)), i = 1; i < t.ticks.length - 1; ++i) g.push(m(t.ticks[i], g))
                }
            })), P(y.setupGrid, [])
        }

        function F(t) {
            var i, n = t.options, o = n.min, a = n.max, r = t.datamin, s = t.datamax;
            switch (n.autoScale) {
                case"none":
                    o = +(null != n.min ? n.min : r), a = +(null != n.max ? n.max : s);
                    break;
                case"loose":
                    if (null != r && null != s) {
                        o = r, a = s, i = e.plot.saturated.saturate(a - o);
                        var l = "number" == typeof n.autoScaleMargin ? n.autoScaleMargin : .02;
                        o = e.plot.saturated.saturate(o - i * l), a = e.plot.saturated.saturate(a + i * l), o < 0 && 0 <= r && (o = 0)
                    } else o = n.min, a = n.max;
                    break;
                case"exact":
                    o = null != r ? r : n.min, a = null != s ? s : n.max;
                    break;
                case"sliding-window":
                    a < s && (a = s, o = Math.max(s - (n.windowSize || 100), o))
            }
            var c = function (e, t) {
                var i = void 0 === e ? null : e, n = void 0 === t ? null : t;
                if (0 == n - i) {
                    var o = 0 === n ? 1 : .01, a = null;
                    null == i && (a -= o), null != n && null == i || (n += o), null != a && (i = a)
                }
                return {min: i, max: n}
            }(o, a);
            o = c.min, a = c.max, !0 === n.growOnly && "none" !== n.autoScale && "sliding-window" !== n.autoScale && (o = o < r ? o : null !== r ? r : o, a = s < a ? a : null !== s ? s : a), t.autoScaledMin = o, t.autoScaledMax = a
        }

        function D(t, i, n, o, a) {
            var r = Y(n, u, o), s = e.plot.saturated.delta(t, i, r), l = -Math.floor(Math.log(s) / Math.LN10);
            a && a < l && (l = a);
            var c = s / parseFloat("1e" + -l);
            return 2.25 < c && c < 3 && (null == a || l + 1 <= a) && ++l, isFinite(l) ? l : 0
        }

        function W(t, i, n, o) {
            var a = e.plot.saturated.delta(t, i, n), r = -Math.floor(Math.log(a) / Math.LN10);
            o && o < r && (r = o);
            var s, l = parseFloat("1e" + -r), c = a / l;
            return c < 1.5 ? s = 1 : c < 3 ? (s = 2, 2.25 < c && (null == o || r + 1 <= o) && (s = 2.5)) : s = c < 7.5 ? 5 : 10, s * l
        }

        function Y(e, t, i) {
            return "number" == typeof i && 0 < i ? i : .3 * Math.sqrt("x" === e ? t.width : t.height)
        }

        function X(e, t, i, n) {
            if (null === t) switch (n) {
                case"min":
                case"max":
                    var o = (a = e, r = i, s = Math.floor(r.p2c(a)), l = "x" === r.direction ? s + 1 : s - 1, D(r.c2p(s), r.c2p(l), r.direction, 1));
                    isFinite(o), t = i.tickFormatter(e, i, o, w);
                    break;
                case"major":
                    t = i.tickFormatter(e, i, void 0, w)
            }
            var a, r, s, l;
            return {v: e, label: t}
        }

        function G() {
            u.clear(), P(y.drawBackground, [d]);
            var e = c.grid;
            e.show && e.backgroundColor && (d.save(), d.translate(v.left, v.top), d.fillStyle = te(c.grid.backgroundColor, b, 0, "rgba(255, 255, 255, 0)"), d.fillRect(0, 0, x, b), d.restore()), e.show && !e.aboveData && Q();
            for (var t = 0; t < l.length; ++t) P(y.drawSeries, [d, l[t], t, te]), U(l[t]);
            P(y.draw, [d]), e.show && e.aboveData && Q(), u.render(), $()
        }

        function B(e, t) {
            for (var i, n, o, a, r = L(), s = 0; s < r.length; ++s) if ((i = r[s]).direction === t && (e[a = t + i.n + "axis"] || 1 !== i.n || (a = t + "axis"), e[a])) {
                n = e[a].from, o = e[a].to;
                break
            }
            if (e[a] || (i = "x" === t ? g[0] : m[0], n = e[t + "1"], o = e[t + "2"]), null != n && null != o && o < n) {
                var l = n;
                n = o, o = l
            }
            return {from: n, to: o, axis: i}
        }

        function j(e) {
            var t = e.box, i = 0, n = 0;
            return "x" === e.direction ? (i = 0, n = t.top - v.top + ("top" === e.position ? t.height : 0)) : (n = 0, i = t.left - v.left + ("left" === e.position ? t.width : 0) + e.boxPosition.centerX), {
                x: i,
                y: n
            }
        }

        function q(e, t) {
            return e % 2 != 0 ? Math.floor(t) + .5 : t
        }

        function H(e) {
            d.lineWidth = 1;
            var t = j(e), i = t.x, n = t.y;
            if (e.show) {
                var o = 0, a = 0;
                d.strokeStyle = e.options.color, d.beginPath(), "x" === e.direction ? o = x + 1 : a = b + 1, "x" === e.direction ? n = q(d.lineWidth, n) : i = q(d.lineWidth, i), d.moveTo(i, n), d.lineTo(i + o, n + a), d.stroke()
            }
        }

        function V(e) {
            var t = e.tickLength, i = e.showMinorTicks, n = M, o = j(e), a = o.x, r = o.y, s = 0;
            for (d.strokeStyle = e.options.color, d.beginPath(), s = 0; s < e.ticks.length; ++s) {
                var l, c = e.ticks[s].v, u = 0, h = 0, p = 0, f = 0;
                if (!isNaN(c) && c >= e.min && c <= e.max && ("x" === e.direction ? (a = e.p2c(c), h = t, "top" === e.position && (h = -h)) : (r = e.p2c(c), u = t, "left" === e.position && (u = -u)), "x" === e.direction ? a = q(d.lineWidth, a) : r = q(d.lineWidth, r), d.moveTo(a, r), d.lineTo(a + u, r + h)), !0 === i && s < e.ticks.length - 1) {
                    var g = e.ticks[s].v, m = (e.ticks[s + 1].v - g) / (n + 1);
                    for (l = 1; l <= n; l++) {
                        if ("x" === e.direction) {
                            if (f = t / 2, a = q(d.lineWidth, e.p2c(g + l * m)), "top" === e.position && (f = -f), a < 0 || x < a) continue
                        } else if (p = t / 2, r = q(d.lineWidth, e.p2c(g + l * m)), "left" === e.position && (p = -p), r < 0 || b < r) continue;
                        d.moveTo(a, r), d.lineTo(a + p, r + f)
                    }
                }
            }
            d.stroke()
        }

        function _(e) {
            var t, i, n;
            for (d.strokeStyle = c.grid.tickColor, d.beginPath(), t = 0; t < e.ticks.length; ++t) {
                var o = e.ticks[t].v, a = 0, r = 0, s = 0, l = 0;
                isNaN(o) || o < e.min || o > e.max || (i = o, n = c.grid.borderWidth, (!("object" === _typeof(n) && 0 < n[e.position] || 0 < n) || i !== e.min && i !== e.max) && ("x" === e.direction ? (s = e.p2c(o), r = -(l = b)) : (s = 0, l = e.p2c(o), a = x), "x" === e.direction ? s = q(d.lineWidth, s) : l = q(d.lineWidth, l), d.moveTo(s, l), d.lineTo(s + a, l + r)))
            }
            d.stroke()
        }

        function Q() {
            var t, i, n, o;
            d.save(), d.translate(v.left, v.top), function () {
                var t, i, n = c.grid.markings;
                if (n) for (e.isFunction(n) && ((t = w.getAxes()).xmin = t.xaxis.min, t.xmax = t.xaxis.max, t.ymin = t.yaxis.min, t.ymax = t.yaxis.max, n = n(t)), i = 0; i < n.length; ++i) {
                    var o = n[i], a = B(o, "x"), r = B(o, "y");
                    if (null == a.from && (a.from = a.axis.min), null == a.to && (a.to = a.axis.max), null == r.from && (r.from = r.axis.min), null == r.to && (r.to = r.axis.max), !(a.to < a.axis.min || a.from > a.axis.max || r.to < r.axis.min || r.from > r.axis.max)) {
                        a.from = Math.max(a.from, a.axis.min), a.to = Math.min(a.to, a.axis.max), r.from = Math.max(r.from, r.axis.min), r.to = Math.min(r.to, r.axis.max);
                        var s = a.from === a.to, l = r.from === r.to;
                        if (!s || !l) if (a.from = Math.floor(a.axis.p2c(a.from)), a.to = Math.floor(a.axis.p2c(a.to)), r.from = Math.floor(r.axis.p2c(r.from)), r.to = Math.floor(r.axis.p2c(r.to)), s || l) {
                            var u = o.lineWidth || c.grid.markingsLineWidth, h = u % 2 ? .5 : 0;
                            d.beginPath(), d.strokeStyle = o.color || c.grid.markingsColor, d.lineWidth = u, s ? (d.moveTo(a.to + h, r.from), d.lineTo(a.to + h, r.to)) : (d.moveTo(a.from, r.to + h), d.lineTo(a.to, r.to + h)), d.stroke()
                        } else d.fillStyle = o.color || c.grid.markingsColor, d.fillRect(a.from, r.to, a.to - a.from, r.from - r.to)
                    }
                }
            }(), t = L(), i = c.grid.borderWidth;
            for (var a = 0; a < t.length; ++a) {
                var r = t[a];
                r.show && (H(r), !0 === r.showTicks && V(r), !0 === r.gridLines && _(r))
            }
            i && (n = c.grid.borderWidth, o = c.grid.borderColor, "object" === _typeof(n) || "object" === _typeof(o) ? ("object" !== _typeof(n) && (n = {
                top: n,
                right: n,
                bottom: n,
                left: n
            }), "object" !== _typeof(o) && (o = {
                top: o,
                right: o,
                bottom: o,
                left: o
            }), 0 < n.top && (d.strokeStyle = o.top, d.lineWidth = n.top, d.beginPath(), d.moveTo(0 - n.left, 0 - n.top / 2), d.lineTo(x, 0 - n.top / 2), d.stroke()), 0 < n.right && (d.strokeStyle = o.right, d.lineWidth = n.right, d.beginPath(), d.moveTo(x + n.right / 2, 0 - n.top), d.lineTo(x + n.right / 2, b), d.stroke()), 0 < n.bottom && (d.strokeStyle = o.bottom, d.lineWidth = n.bottom, d.beginPath(), d.moveTo(x + n.right, b + n.bottom / 2), d.lineTo(0, b + n.bottom / 2), d.stroke()), 0 < n.left && (d.strokeStyle = o.left, d.lineWidth = n.left, d.beginPath(), d.moveTo(0 - n.left / 2, b + n.bottom), d.lineTo(0 - n.left / 2, 0), d.stroke())) : (d.lineWidth = n, d.strokeStyle = c.grid.borderColor, d.strokeRect(-n / 2, -n / 2, x + n, b + n))), d.restore()
        }

        function U(t) {
            t.lines.show && e.plot.drawSeries.drawSeriesLines(t, d, v, x, b, w.drawSymbol, te), t.bars.show && e.plot.drawSeries.drawSeriesBars(t, d, v, x, b, w.drawSymbol, te), t.points.show && e.plot.drawSeries.drawSeriesPoints(t, d, v, x, b, w.drawSymbol, te)
        }

        function Z(e, t, i, n, o) {
            for (var a = function (e, t, i, n, o) {
                var a, r = [], s = [], c = n * n + 1;
                for (a = l.length - 1; 0 <= a; --a) if (i(a)) {
                    var u = l[a];
                    if (!u.datapoints) return;
                    var h = !1;
                    if (u.lines.show || u.points.show) {
                        var p = J(u, e, t, n, o);
                        p && (s.push({seriesIndex: a, dataIndex: p.dataIndex, distance: p.distance}), h = !0)
                    }
                    if (u.bars.show && !h) {
                        var d = K(u, e, t);
                        0 <= d && s.push({seriesIndex: a, dataIndex: d, distance: c})
                    }
                }
                for (a = 0; a < s.length; a++) {
                    var f = s[a].seriesIndex, g = s[a].dataIndex, m = s[a].distance, v = l[f].datapoints.pointsize;
                    r.push({
                        datapoint: l[f].datapoints.points.slice(g * v, (g + 1) * v),
                        dataIndex: g,
                        series: l[f],
                        seriesIndex: f,
                        distance: Math.sqrt(m)
                    })
                }
                return r
            }(e, t, i, n, o), r = 0; r < l.length; ++r) i(r) && P(y.findNearbyItems, [e, t, l, r, n, o, a]);
            return a.sort((function (e, t) {
                return void 0 === t.distance ? -1 : void 0 === e.distance && void 0 !== t.distance ? 1 : e.distance - t.distance
            }))
        }

        function J(e, t, i, n, o) {
            var a = e.xaxis.c2p(t), r = e.yaxis.c2p(i), s = n / e.xaxis.scale, l = n / e.yaxis.scale,
                c = e.datapoints.points, u = e.datapoints.pointsize, h = Number.POSITIVE_INFINITY;
            e.xaxis.options.inverseTransform && (s = Number.MAX_VALUE), e.yaxis.options.inverseTransform && (l = Number.MAX_VALUE);
            for (var p = null, d = 0; d < c.length; d += u) {
                var f = c[d], g = c[d + 1];
                if (null != f && !(s < f - a || f - a < -s || l < g - r || g - r < -l)) {
                    var m = Math.abs(e.xaxis.p2c(f) - t), v = Math.abs(e.yaxis.p2c(g) - i),
                        x = o ? o(m, v) : m * m + v * v;
                    x < h && (p = {dataIndex: d / u, distance: h = x})
                }
            }
            return p
        }

        function K(e, t, i) {
            var n, o, a = e.bars.barWidth[0] || e.bars.barWidth, r = e.xaxis.c2p(t), s = e.yaxis.c2p(i),
                l = e.datapoints.points, c = e.datapoints.pointsize;
            switch (e.bars.align) {
                case"left":
                    n = 0;
                    break;
                case"right":
                    n = -a;
                    break;
                default:
                    n = -a / 2
            }
            o = n + a;
            for (var u = e.bars.fillTowards || 0, h = u > e.yaxis.min ? Math.min(e.yaxis.max, u) : e.yaxis.min, p = -1, d = 0; d < l.length; d += c) {
                var f = l[d], g = l[d + 1];
                if (null != f) {
                    var m = 3 === c ? l[d + 2] : h;
                    (e.bars.horizontal ? r <= Math.max(m, f) && r >= Math.min(m, f) && g + n <= s && s <= g + o : f + n <= r && r <= f + o && s >= Math.min(m, g) && s <= Math.max(m, g)) && (p = d / c)
                }
            }
            return p
        }

        function $() {
            var e = c.interaction.redrawOverlayInterval;
            -1 !== e ? T || (T = setTimeout((function () {
                ee(w)
            }), e)) : ee()
        }

        function ee(e) {
            if (T = null, f) {
                h.clear(), P(y.drawOverlay, [f, h]);
                var t = new CustomEvent("onDrawingDone");
                e.getEventHolder().dispatchEvent(t), e.getPlaceholder().trigger("drawingdone")
            }
        }

        function te(t, i, n, o) {
            if ("string" == typeof t) return t;
            for (var a = d.createLinearGradient(0, n, 0, i), r = 0, s = t.colors.length; r < s; ++r) {
                var l = t.colors[r];
                if ("string" != typeof l) {
                    var c = e.color.parse(o);
                    null != l.brightness && (c = c.scale("rgb", l.brightness)), null != l.opacity && (c.a *= l.opacity), l = c.toString()
                }
                a.addColorStop(r / (s - 1), l)
            }
            return a
        }

        !function () {
            for (var i = {Canvas: t}, n = 0; n < s.length; ++n) {
                var o = s[n];
                o.init(w, i), o.options && e.extend(!0, c, o.options)
            }
        }(), function () {
            o.css("padding", 0).children().filter((function () {
                return !e(this).hasClass("flot-overlay") && !e(this).hasClass("flot-base")
            })).remove(), "static" === o.css("position") && o.css("position", "relative"), u = new t("flot-base", o[0]), h = new t("flot-overlay", o[0]), d = u.context, f = h.context, p = e(h.element).unbind();
            var i = o.data("plot");
            i && (i.shutdown(), h.clear()), o.data("plot", w)
        }(), function (t) {
            e.extend(!0, c, t), t && t.colors && (c.colors = t.colors), null == c.xaxis.color && (c.xaxis.color = e.color.parse(c.grid.color).scale("a", .22).toString()), null == c.yaxis.color && (c.yaxis.color = e.color.parse(c.grid.color).scale("a", .22).toString()), null == c.xaxis.tickColor && (c.xaxis.tickColor = c.grid.tickColor || c.xaxis.color), null == c.yaxis.tickColor && (c.yaxis.tickColor = c.grid.tickColor || c.yaxis.color), null == c.grid.borderColor && (c.grid.borderColor = c.grid.color), null == c.grid.tickColor && (c.grid.tickColor = e.color.parse(c.grid.color).scale("a", .22).toString());
            var i, n, a, r = o.css("font-size"), s = r ? +r.replace("px", "") : 13, l = {
                style: o.css("font-style"),
                size: Math.round(.8 * s),
                variant: o.css("font-variant"),
                weight: o.css("font-weight"),
                family: o.css("font-family")
            };
            for (a = c.xaxes.length || 1, i = 0; i < a; ++i) (n = c.xaxes[i]) && !n.tickColor && (n.tickColor = n.color), n = e.extend(!0, {}, c.xaxis, n), (c.xaxes[i] = n).font && (n.font = e.extend({}, l, n.font), n.font.color || (n.font.color = n.color), n.font.lineHeight || (n.font.lineHeight = Math.round(1.15 * n.font.size)));
            for (a = c.yaxes.length || 1, i = 0; i < a; ++i) (n = c.yaxes[i]) && !n.tickColor && (n.tickColor = n.color), n = e.extend(!0, {}, c.yaxis, n), (c.yaxes[i] = n).font && (n.font = e.extend({}, l, n.font), n.font.color || (n.font.color = n.color), n.font.lineHeight || (n.font.lineHeight = Math.round(1.15 * n.font.size)));
            for (i = 0; i < c.xaxes.length; ++i) z(g, i + 1).options = c.xaxes[i];
            for (i = 0; i < c.yaxes.length; ++i) z(m, i + 1).options = c.yaxes[i];
            for (var u in e.each(L(), (function (e, t) {
                t.boxPosition = t.options.boxPosition || {centerX: 0, centerY: 0}
            })), y) c.hooks[u] && c.hooks[u].length && (y[u] = y[u].concat(c.hooks[u]));
            P(y.processOptions, [c])
        }(r), C(a), R(!0), G(), P(y.bindEvents, [p])
    }

    e.plot = function (t, i, n) {
        return new r(e(t), i, n, e.plot.plugins)
    }, e.plot.version = "3.0.0", e.plot.plugins = [], e.fn.plot = function (t, i) {
        return this.each((function () {
            e.plot(this, t, i)
        }))
    }, e.plot.linearTickGenerator = i, e.plot.defaultTickFormatter = n, e.plot.expRepTickFormatter = o
}(jQuery), function (e) {
    var t = {
        saturate: function (e) {
            return e === 1 / 0 ? Number.MAX_VALUE : e === -1 / 0 ? -Number.MAX_VALUE : e
        }, delta: function (e, t, i) {
            return (t - e) / i == 1 / 0 ? t / i - e / i : (t - e) / i
        }, multiply: function (e, i) {
            return t.saturate(e * i)
        }, multiplyAdd: function (e, i, n) {
            if (isFinite(e * i)) return t.saturate(e * i + n);
            for (var o = n, a = 0; a < i; a++) o += e;
            return t.saturate(o)
        }, floorInBase: function (e, t) {
            return t * Math.floor(e / t)
        }
    };
    e.plot.saturated = t
}(jQuery), function (e) {
    var t = {
        getPageXY: function (e) {
            var t = document.documentElement;
            return {
                X: e.clientX + (window.pageXOffset || t.scrollLeft) - (t.clientLeft || 0),
                Y: e.clientY + (window.pageYOffset || t.scrollTop) - (t.clientTop || 0)
            }
        }, getPixelRatio: function (e) {
            return (window.devicePixelRatio || 1) / (e.webkitBackingStorePixelRatio || e.mozBackingStorePixelRatio || e.msBackingStorePixelRatio || e.oBackingStorePixelRatio || e.backingStorePixelRatio || 1)
        }, isSafari: function () {
            return /constructor/i.test(window.top.HTMLElement) || "[object SafariRemoteNotification]" === (!window.top.safari || void 0 !== window.top.safari && window.top.safari.pushNotification).toString()
        }, isMobileSafari: function () {
            return navigator.userAgent.match(/(iPod|iPhone|iPad)/) && navigator.userAgent.match(/AppleWebKit/)
        }, isOpera: function () {
            return !!window.opr && !!opr.addons || !!window.opera || 0 <= navigator.userAgent.indexOf(" OPR/")
        }, isFirefox: function () {
            return "undefined" != typeof InstallTrigger
        }, isIE: function () {
            return !!document.documentMode
        }, isEdge: function () {
            return !t.isIE() && !!window.StyleMedia
        }, isChrome: function () {
            return !!window.chrome && !!window.chrome.webstore
        }, isBlink: function () {
            return (t.isChrome() || t.isOpera()) && !!window.CSS
        }
    };
    e.plot.browser = t
}(jQuery), function (e) {
    e.plot.drawSeries = new function () {
        function t(e, t, i, n, o, a, r, s, l, c, u) {
            var h, p, d, f, g = e + n, m = e + o, v = i, x = t, b = !1;
            h = p = d = !0, c ? (b = p = d = !0, h = !1, x = t + n, v = t + o, (m = e) < (g = i) && (f = m, m = g, g = f, p = !(h = !0))) : (h = p = d = !0, b = !1, g = e + n, m = e + o, (x = t) < (v = i) && (f = x, x = v, v = f, d = !(b = !0))), m < r.min || g > r.max || x < s.min || v > s.max || (g < r.min && (g = r.min, h = !1), m > r.max && (m = r.max, p = !1), v < s.min && (v = s.min, b = !1), x > s.max && (x = s.max, d = !1), g = r.p2c(g), v = s.p2c(v), m = r.p2c(m), x = s.p2c(x), a && (l.fillStyle = a(v, x), l.fillRect(g, x, m - g, v - x)), 0 < u && (h || p || d || b) && (l.beginPath(), l.moveTo(g, v), h ? l.lineTo(g, x) : l.moveTo(g, x), d ? l.lineTo(m, x) : l.moveTo(m, x), p ? l.lineTo(m, v) : l.moveTo(m, v), b ? l.lineTo(g, v) : l.moveTo(g, v), l.stroke()))
        }

        function i(t, i, n, o, a) {
            var r = t.fill;
            if (!r) return null;
            if (t.fillColor) return a(t.fillColor, n, o, i);
            var s = e.color.parse(i);
            return s.a = "number" == typeof r ? r : .4, s.normalize(), s.toString()
        }

        this.drawSeriesLines = function (e, t, n, o, a, r, s) {
            t.save(), t.translate(n.left, n.top), t.lineJoin = "round", e.lines.dashes && t.setLineDash && t.setLineDash(e.lines.dashes);
            var l = {format: e.datapoints.format, points: e.datapoints.points, pointsize: e.datapoints.pointsize};
            e.decimate && (l.points = e.decimate(e, e.xaxis.min, e.xaxis.max, o, e.yaxis.min, e.yaxis.max, a));
            var c = e.lines.lineWidth;
            t.lineWidth = c, t.strokeStyle = e.color;
            var u = i(e.lines, e.color, 0, a, s);
            u && (t.fillStyle = u, function (e, t, i, n, o, a) {
                for (var r = e.points, s = e.pointsize, l = n > i.min ? Math.min(i.max, n) : i.min, c = 0, u = 1, h = !1, p = 0, d = 0, f = null, g = null; !(0 < s && c > r.length + s);) {
                    var m = r[(c += s) - s], v = r[c - s + u], x = r[c], b = r[c + u];
                    if (-2 === s && (v = b = l), h) {
                        if (0 < s && null != m && null == x) {
                            d = c, s = -s, u = 2;
                            continue
                        }
                        if (s < 0 && c === p + s) {
                            o.fill(), h = !1, u = 1, c = p = d + (s = -s);
                            continue
                        }
                    }
                    if (null != m && null != x) {
                        if (a && (null !== f && null !== g ? (x = m, b = v, m = f, v = g, g = f = null, c -= s) : v !== b && m !== x && (f = x, g = b = v)), m <= x && m < t.min) {
                            if (x < t.min) continue;
                            v = (t.min - m) / (x - m) * (b - v) + v, m = t.min
                        } else if (x <= m && x < t.min) {
                            if (m < t.min) continue;
                            b = (t.min - m) / (x - m) * (b - v) + v, x = t.min
                        }
                        if (x <= m && m > t.max) {
                            if (x > t.max) continue;
                            v = (t.max - m) / (x - m) * (b - v) + v, m = t.max
                        } else if (m <= x && x > t.max) {
                            if (m > t.max) continue;
                            b = (t.max - m) / (x - m) * (b - v) + v, x = t.max
                        }
                        if (h || (o.beginPath(), o.moveTo(t.p2c(m), i.p2c(l)), h = !0), v >= i.max && b >= i.max) o.lineTo(t.p2c(m), i.p2c(i.max)), o.lineTo(t.p2c(x), i.p2c(i.max)); else if (v <= i.min && b <= i.min) o.lineTo(t.p2c(m), i.p2c(i.min)), o.lineTo(t.p2c(x), i.p2c(i.min)); else {
                            var y = m, w = x;
                            v <= b && v < i.min && b >= i.min ? (m = (i.min - v) / (b - v) * (x - m) + m, v = i.min) : b <= v && b < i.min && v >= i.min && (x = (i.min - v) / (b - v) * (x - m) + m, b = i.min), b <= v && v > i.max && b <= i.max ? (m = (i.max - v) / (b - v) * (x - m) + m, v = i.max) : v <= b && b > i.max && v <= i.max && (x = (i.max - v) / (b - v) * (x - m) + m, b = i.max), m !== y && o.lineTo(t.p2c(y), i.p2c(v)), o.lineTo(t.p2c(m), i.p2c(v)), o.lineTo(t.p2c(x), i.p2c(b)), x !== w && (o.lineTo(t.p2c(x), i.p2c(b)), o.lineTo(t.p2c(w), i.p2c(b)))
                        }
                    } else g = f = null
                }
            }(l, e.xaxis, e.yaxis, e.lines.fillTowards || 0, t, e.lines.steps)), 0 < c && function (e, t, i, n, o, a, r) {
                var s = e.points, l = e.pointsize, c = null, u = null, h = 0, p = 0, d = 0, f = 0, g = null, m = null,
                    v = 0;
                for (a.beginPath(), v = l; v < s.length; v += l) if (h = s[v - l], p = s[v - l + 1], d = s[v], f = s[v + 1], null !== h && null !== d) if (isNaN(h) || isNaN(d) || isNaN(p) || isNaN(f)) u = c = null; else {
                    if (r && (null !== g && null !== m ? (d = h, f = p, h = g, p = m, m = g = null, v -= l) : p !== f && h !== d && (g = d, m = f = p)), p <= f && p < o.min) {
                        if (f < o.min) continue;
                        h = (o.min - p) / (f - p) * (d - h) + h, p = o.min
                    } else if (f <= p && f < o.min) {
                        if (p < o.min) continue;
                        d = (o.min - p) / (f - p) * (d - h) + h, f = o.min
                    }
                    if (f <= p && p > o.max) {
                        if (f > o.max) continue;
                        h = (o.max - p) / (f - p) * (d - h) + h, p = o.max
                    } else if (p <= f && f > o.max) {
                        if (p > o.max) continue;
                        d = (o.max - p) / (f - p) * (d - h) + h, f = o.max
                    }
                    if (h <= d && h < n.min) {
                        if (d < n.min) continue;
                        p = (n.min - h) / (d - h) * (f - p) + p, h = n.min
                    } else if (d <= h && d < n.min) {
                        if (h < n.min) continue;
                        f = (n.min - h) / (d - h) * (f - p) + p, d = n.min
                    }
                    if (d <= h && h > n.max) {
                        if (d > n.max) continue;
                        p = (n.max - h) / (d - h) * (f - p) + p, h = n.max
                    } else if (h <= d && d > n.max) {
                        if (h > n.max) continue;
                        f = (n.max - h) / (d - h) * (f - p) + p, d = n.max
                    }
                    h === c && p === u || a.moveTo(n.p2c(h) + 0, o.p2c(p) + 0), c = d, u = f, a.lineTo(n.p2c(d) + 0, o.p2c(f) + 0)
                } else m = g = null;
                a.stroke()
            }(l, 0, 0, e.xaxis, e.yaxis, t, e.lines.steps), t.restore()
        }, this.drawSeriesPoints = function (e, t, n, o, a, r, s) {
            function l(e, t, i, n, o, a) {
                e.moveTo(t + n, i), e.arc(t, i, n, 0, o ? Math.PI : 2 * Math.PI, !1)
            }

            l.fill = !0, t.save(), t.translate(n.left, n.top);
            var c = {format: e.datapoints.format, points: e.datapoints.points, pointsize: e.datapoints.pointsize};
            e.decimatePoints && (c.points = e.decimatePoints(e, e.xaxis.min, e.xaxis.max, o, e.yaxis.min, e.yaxis.max, a));
            var u, h = e.points.lineWidth, p = e.points.radius, d = e.points.symbol;
            "circle" === d ? u = l : "string" == typeof d && r && r[d] ? u = r[d] : "function" == typeof r && (u = r), 0 === h && (h = 1e-4), t.lineWidth = h, t.fillStyle = i(e.points, e.color, null, null, s), t.strokeStyle = e.color, function (e, i, n, o, a, r, s, l) {
                var c = e.points, u = e.pointsize;
                t.beginPath();
                for (var h = 0; h < c.length; h += u) {
                    var p = c[h], d = c[h + 1];
                    null == p || p < r.min || p > r.max || d < s.min || d > s.max || (p = r.p2c(p), d = s.p2c(d) + 0, l(t, p, d, i, false, true))
                }
                l.fill && t.fill(), t.stroke()
            }(c, p, 0, 0, 0, e.xaxis, e.yaxis, u), t.restore()
        }, this.drawSeriesBars = function (e, n, o, a, r, s, l) {
            n.save(), n.translate(o.left, o.top);
            var c, u = {format: e.datapoints.format, points: e.datapoints.points, pointsize: e.datapoints.pointsize};
            e.decimate && (u.points = e.decimate(e, e.xaxis.min, e.xaxis.max, a)), n.lineWidth = e.bars.lineWidth, n.strokeStyle = e.color;
            var h = e.bars.barWidth[0] || e.bars.barWidth;
            switch (e.bars.align) {
                case"left":
                    c = 0;
                    break;
                case"right":
                    c = -h;
                    break;
                default:
                    c = -h / 2
            }
            !function (i, o, a, r, s, l) {
                for (var c = i.points, u = i.pointsize, h = e.bars.fillTowards || 0, p = h > l.min ? Math.min(l.max, h) : l.min, d = 0; d < c.length; d += u) if (null != c[d]) {
                    var f = 3 === u ? c[d + 2] : p;
                    t(c[d], c[d + 1], f, o, a, r, s, l, n, e.bars.horizontal, e.bars.lineWidth)
                }
            }(u, c, c + h, e.bars.fill ? function (t, n) {
                return i(e.bars, e.color, t, n, l)
            } : null, e.xaxis, e.yaxis), n.restore()
        }, this.drawBar = t
    }
}(jQuery), function (e) {
    function t(e, t, i, n) {
        if (t.points.errorbars) {
            var o = [{x: !0, number: !0, required: !0}, {y: !0, number: !0, required: !0}], a = t.points.errorbars;
            "x" !== a && "xy" !== a || (t.points.xerr.asymmetric && o.push({
                x: !0,
                number: !0,
                required: !0
            }), o.push({
                x: !0,
                number: !0,
                required: !0
            })), "y" !== a && "xy" !== a || (t.points.yerr.asymmetric && o.push({
                y: !0,
                number: !0,
                required: !0
            }), o.push({y: !0, number: !0, required: !0})), n.format = o
        }
    }

    function i(e, t) {
        var i = e.datapoints.points, n = null, o = null, a = null, r = null, s = e.points.xerr, l = e.points.yerr,
            c = e.points.errorbars;
        "x" === c || "xy" === c ? s.asymmetric ? (n = i[t + 2], o = i[t + 3], "xy" === c && (l.asymmetric ? (a = i[t + 4], r = i[t + 5]) : a = i[t + 4])) : (n = i[t + 2], "xy" === c && (l.asymmetric ? (a = i[t + 3], r = i[t + 4]) : a = i[t + 3])) : "y" === c && (l.asymmetric ? (a = i[t + 2], r = i[t + 3]) : a = i[t + 2]), null == o && (o = n), null == r && (r = a);
        var u = [n, o, a, r];
        return s.show || (u[0] = null, u[1] = null), l.show || (u[2] = null, u[3] = null), u
    }

    function n(t, i, n, a, r, s, l, c, u, h, p) {
        a += h, r += h, s += h, "x" === i.err ? (n + u < r ? o(t, [[r, a], [Math.max(n + u, p[0]), a]]) : l = !1, s < n - u ? o(t, [[Math.min(n - u, p[1]), a], [s, a]]) : c = !1) : (r < a - u ? o(t, [[n, r], [n, Math.min(a - u, p[0])]]) : l = !1, a + u < s ? o(t, [[n, Math.max(a + u, p[1])], [n, s]]) : c = !1), u = null != i.radius ? i.radius : u, l && ("-" === i.upperCap ? "x" === i.err ? o(t, [[r, a - u], [r, a + u]]) : o(t, [[n - u, r], [n + u, r]]) : e.isFunction(i.upperCap) && ("x" === i.err ? i.upperCap(t, r, a, u) : i.upperCap(t, n, r, u))), c && ("-" === i.lowerCap ? "x" === i.err ? o(t, [[s, a - u], [s, a + u]]) : o(t, [[n - u, s], [n + u, s]]) : e.isFunction(i.lowerCap) && ("x" === i.err ? i.lowerCap(t, s, a, u) : i.lowerCap(t, n, s, u)))
    }

    function o(e, t) {
        e.beginPath(), e.moveTo(t[0][0], t[0][1]);
        for (var i = 1; i < t.length; i++) e.lineTo(t[i][0], t[i][1]);
        e.stroke()
    }

    function a(t, o) {
        var a = t.getPlotOffset();
        o.save(), o.translate(a.left, a.top), e.each(t.getData(), (function (e, t) {
            t.points.errorbars && (t.points.xerr.show || t.points.yerr.show) && function (e, t, o) {
                var a, r = o.datapoints.points, s = o.datapoints.pointsize, l = [o.xaxis, o.yaxis], c = o.points.radius,
                    u = [o.points.xerr, o.points.yerr], h = !1;
                l[0].p2c(l[0].max) < l[0].p2c(l[0].min) && (h = !0, a = u[0].lowerCap, u[0].lowerCap = u[0].upperCap, u[0].upperCap = a);
                var p = !1;
                l[1].p2c(l[1].min) < l[1].p2c(l[1].max) && (p = !0, a = u[1].lowerCap, u[1].lowerCap = u[1].upperCap, u[1].upperCap = a);
                for (var d = 0; d < o.datapoints.points.length; d += s) for (var f = i(o, d), g = 0; g < u.length; g++) {
                    var m = [l[g].min, l[g].max];
                    if (f[g * u.length]) {
                        var v = r[d], x = r[d + 1], b = [v, x][g] + f[g * u.length + 1],
                            y = [v, x][g] - f[g * u.length];
                        if ("x" === u[g].err && (x > l[1].max || x < l[1].min || b < l[0].min || y > l[0].max)) continue;
                        if ("y" === u[g].err && (v > l[0].max || v < l[0].min || b < l[1].min || y > l[1].max)) continue;
                        var w = !0, k = !0;
                        b > m[1] && (w = !1, b = m[1]), y < m[0] && (k = !1, y = m[0]), ("x" === u[g].err && h || "y" === u[g].err && p) && (a = y, y = b, b = a, a = k, k = w, w = a, a = m[0], m[0] = m[1], m[1] = a), v = l[0].p2c(v), x = l[1].p2c(x), b = l[g].p2c(b), y = l[g].p2c(y), m[0] = l[g].p2c(m[0]), m[1] = l[g].p2c(m[1]);
                        var T = u[g].lineWidth ? u[g].lineWidth : o.points.lineWidth,
                            M = null != o.points.shadowSize ? o.points.shadowSize : o.shadowSize;
                        if (0 < T && 0 < M) {
                            var S = M / 2;
                            t.lineWidth = S, t.strokeStyle = "rgba(0,0,0,0.1)", n(t, u[g], v, x, b, y, w, k, c, S + S / 2, m), t.strokeStyle = "rgba(0,0,0,0.2)", n(t, u[g], v, x, b, y, w, k, c, S / 2, m)
                        }
                        t.strokeStyle = u[g].color ? u[g].color : o.color, t.lineWidth = T, n(t, u[g], v, x, b, y, w, k, c, 0, m)
                    }
                }
            }(0, o, t)
        })), o.restore()
    }

    e.plot.plugins.push({
        init: function (e) {
            e.hooks.processRawData.push(t), e.hooks.draw.push(a)
        },
        options: {
            series: {
                points: {
                    errorbars: null,
                    xerr: {
                        err: "x",
                        show: null,
                        asymmetric: null,
                        upperCap: null,
                        lowerCap: null,
                        color: null,
                        radius: null
                    },
                    yerr: {
                        err: "y",
                        show: null,
                        asymmetric: null,
                        upperCap: null,
                        lowerCap: null,
                        color: null,
                        radius: null
                    }
                }
            }
        },
        name: "errorbars",
        version: "1.0"
    })
}(jQuery), jQuery.plot.uiConstants = {
    SNAPPING_CONSTANT: 20,
    PANHINT_LENGTH_CONSTANT: 10,
    MINOR_TICKS_COUNT_CONSTANT: 4,
    TICK_LENGTH_CONSTANT: 10,
    ZOOM_DISTANCE_MARGIN: 25
}, function (e) {
    var t = n(Number.MAX_VALUE, 10), i = n(Number.MAX_VALUE, 4);

    function n(e, t) {
        for (var i, n, o = Math.floor(Math.log(e) * Math.LOG10E) - 1, a = [], r = -o; r <= o; r++) {
            n = parseFloat("1e" + r);
            for (var s = 1; s < 9; s += t) i = n * s, a.push(i)
        }
        return a
    }

    var o = function (n, o, r) {
        var s = [], l = -1, c = -1, u = n.getCanvas(), h = t, p = a(o, n), d = o.max;
        r || (r = .3 * Math.sqrt("x" === o.direction ? u.width : u.height)), t.some((function (e, t) {
            return p <= e && (l = t, !0)
        })), t.some((function (e, t) {
            return d <= e && (c = t, !0)
        })), -1 === c && (c = t.length - 1), c - l <= r / 4 && h.length !== i.length && (h = i, l *= 2, c *= 2);
        var f, g, m, v = null, x = 1 / r;
        if (r / 4 <= c - l) {
            for (var b = c; l <= b; b--) f = h[b], g = (Math.log(f) - Math.log(p)) / (Math.log(d) - Math.log(p)), m = f, null === v ? v = {
                pixelCoord: g,
                idealPixelCoord: g
            } : Math.abs(g - v.pixelCoord) >= x ? v = {
                pixelCoord: g,
                idealPixelCoord: v.idealPixelCoord - x
            } : m = null, m && s.push(m);
            s.reverse()
        } else {
            var y = n.computeTickSize(p, d, r), w = {min: p, max: d, tickSize: y};
            s = e.plot.linearTickGenerator(w)
        }
        return s
    }, a = function (e, t) {
        var i = e.min, n = e.max;
        return i <= 0 && n < (i = null === e.datamin ? e.min = .1 : d(t, e)) && (e.max = null !== e.datamax ? e.datamax : e.options.max, e.options.offset.below = 0, e.options.offset.above = 0), i
    }, r = function (t, i, n) {
        var o = 0 < t ? Math.floor(Math.log(t) / Math.LN10) : 0;
        if (n) return -4 <= o && o <= 7 ? e.plot.defaultTickFormatter(t, i, n) : e.plot.expRepTickFormatter(t, i, n);
        if (-4 <= o && o <= 7) {
            var a = o < 0 ? t.toFixed(-o) : t.toFixed(o + 2);
            if (-1 !== a.indexOf(".")) {
                for (var r = a.lastIndexOf("0"); r === a.length - 1;) r = (a = a.slice(0, -1)).lastIndexOf("0");
                a.indexOf(".") === a.length - 1 && (a = a.slice(0, -1))
            }
            return a
        }
        return e.plot.expRepTickFormatter(t, i)
    }, s = function (e) {
        return e < t[0] && (e = t[0]), Math.log(e)
    }, l = function (e) {
        return Math.exp(e)
    }, c = function (e) {
        return -e
    }, u = function (e) {
        return -s(e)
    }, h = function (e) {
        return l(-e)
    };

    function p(e, t) {
        "log" === t.options.mode && t.datamin <= 0 && (null === t.datamin ? t.datamin = .1 : t.datamin = d(e, t))
    }

    function d(e, t) {
        var i = e.getData().filter((function (e) {
                return e.xaxis === t || e.yaxis === t
            })).map((function (t) {
                return e.computeRangeForDataSeries(t, null, f)
            })),
            n = "x" === t.direction ? Math.min(.1, i && i[0] ? i[0].xmin : .1) : Math.min(.1, i && i[0] ? i[0].ymin : .1);
        return t.min = n
    }

    function f(e) {
        return 0 < e
    }

    e.plot.plugins.push({
        init: function (t) {
            t.hooks.processOptions.push((function (t) {
                e.each(t.getAxes(), (function (e, i) {
                    var n = i.options;
                    "log" === n.mode ? (i.tickGenerator = function (e) {
                        return o(t, e, 11)
                    }, "function" != typeof i.options.tickFormatter && (i.options.tickFormatter = r), i.options.transform = n.inverted ? u : s, i.options.inverseTransform = n.inverted ? h : l, i.options.autoScaleMargin = 0, t.hooks.setRange.push(p)) : n.inverted && (i.options.transform = c, i.options.inverseTransform = c)
                }))
            }))
        }, options: {xaxis: {}}, name: "log", version: "0.1"
    }), e.plot.logTicksGenerator = o, e.plot.logTickFormatter = r
}(jQuery), function (e) {
    var t = function (e, t, i, n, o) {
        var a = n * Math.sqrt(Math.PI) / 2;
        e.rect(t - a, i - a, a + a, a + a)
    }, i = function (e, t, i, n, o) {
        var a = n * Math.sqrt(Math.PI) / 2;
        e.rect(t - a, i - a, a + a, a + a)
    }, n = function (e, t, i, n, o) {
        var a = n * Math.sqrt(Math.PI / 2);
        e.moveTo(t - a, i), e.lineTo(t, i - a), e.lineTo(t + a, i), e.lineTo(t, i + a), e.lineTo(t - a, i), e.lineTo(t, i - a)
    }, o = function (e, t, i, n, o) {
        var a = n * Math.sqrt(2 * Math.PI / Math.sin(Math.PI / 3)), r = a * Math.sin(Math.PI / 3);
        e.moveTo(t - a / 2, i + r / 2), e.lineTo(t + a / 2, i + r / 2), o || (e.lineTo(t, i - r / 2), e.lineTo(t - a / 2, i + r / 2), e.lineTo(t + a / 2, i + r / 2))
    }, a = function (e, t, i, n, o, a) {
        o || (e.moveTo(t + n, i), e.arc(t, i, n, 0, 2 * Math.PI, !1))
    }, r = {
        square: t, rectangle: i, diamond: n, triangle: o, cross: function (e, t, i, n, o) {
            var a = n * Math.sqrt(Math.PI) / 2;
            e.moveTo(t - a, i - a), e.lineTo(t + a, i + a), e.moveTo(t - a, i + a), e.lineTo(t + a, i - a)
        }, ellipse: a, plus: function (e, t, i, n, o) {
            var a = n * Math.sqrt(Math.PI / 2);
            e.moveTo(t - a, i), e.lineTo(t + a, i), e.moveTo(t, i + a), e.lineTo(t, i - a)
        }
    };
    a.fill = o.fill = n.fill = i.fill = t.fill = !0, e.plot.plugins.push({
        init: function (e) {
            e.drawSymbol = r
        }, name: "symbols", version: "1.0"
    })
}(jQuery), function (e) {
    function t(e, t, i, n) {
        if (!0 === t.flatdata) {
            var o = t.start || 0, a = "number" == typeof t.step ? t.step : 1;
            n.pointsize = 2;
            for (var r = 0, s = 0; r < i.length; r++, s += 2) n.points[s] = o + r * a, n.points[s + 1] = i[r];
            void 0 !== n.points ? n.points.length = 2 * i.length : n.points = []
        }
    }

    jQuery.plot.plugins.push({
        init: function (e) {
            e.hooks.processRawData.push(t)
        }, name: "flatdata", version: "0.0.2"
    })
}(), function (e) {
    var t = e.plot.saturated, i = e.plot.browser, n = e.plot.uiConstants.SNAPPING_CONSTANT,
        o = e.plot.uiConstants.PANHINT_LENGTH_CONSTANT;

    function a(a, r) {
        var s, l = null, c = !1, u = "manual" === r.pan.mode, h = "smartLock" === r.pan.mode,
            p = h || "smart" === r.pan.mode, d = "default", f = null, g = null, m = {x: 0, y: 0}, v = !1;

        function x(e, t) {
            var n = Math.abs(e.originalEvent.deltaY) <= 1 ? 1 + Math.abs(e.originalEvent.deltaY) / 50 : null;
            if (v && T(e), a.getOptions().zoom.active) return e.preventDefault(), function (e, t, n) {
                var o = i.getPageXY(e), r = a.offset();
                r.left = o.X - r.left, r.top = o.Y - r.top;
                var s = a.getPlaceholder().offset();
                s.left = o.X - s.left, s.top = o.Y - s.top;
                var l = a.getXAxes().concat(a.getYAxes()).filter((function (e) {
                    var t = e.box;
                    if (void 0 !== t) return s.left > t.left && s.left < t.left + t.width && s.top > t.top && s.top < t.top + t.height
                }));
                0 === l.length && (l = void 0), t ? a.zoomOut({center: r, axes: l, amount: n}) : a.zoom({
                    center: r,
                    axes: l,
                    amount: n
                })
            }(e, t < 0, n), !1
        }

        function b(e) {
            c = !0
        }

        function y(e) {
            c = !1
        }

        function w(e) {
            if (!c || 0 !== e.button) return !1;
            v = !0;
            var t = i.getPageXY(e), n = a.getPlaceholder().offset();
            n.left = t.X - n.left, n.top = t.Y - n.top, 0 === (l = a.getXAxes().concat(a.getYAxes()).filter((function (e) {
                var t = e.box;
                if (void 0 !== t) return n.left > t.left && n.left < t.left + t.width && n.top > t.top && n.top < t.top + t.height
            }))).length && (l = void 0);
            var o = a.getPlaceholder().css("cursor");
            o && (d = o), a.getPlaceholder().css("cursor", a.getOptions().pan.cursor), p ? s = a.navigationState(t.X, t.Y) : u && (m.x = t.X, m.y = t.Y)
        }

        function k(e) {
            if (v) {
                var t = i.getPageXY(e), n = a.getOptions().pan.frameRate;
                -1 !== n ? !g && n && (g = setTimeout((function () {
                    p ? a.smartPan({
                        x: s.startPageX - t.X,
                        y: s.startPageY - t.Y
                    }, s, l, !1, h) : u && (a.pan({
                        left: m.x - t.X,
                        top: m.y - t.Y,
                        axes: l
                    }), m.x = t.X, m.y = t.Y), g = null
                }), 1 / n * 1e3)) : p ? a.smartPan({
                    x: s.startPageX - t.X,
                    y: s.startPageY - t.Y
                }, s, l, !1, h) : u && (a.pan({left: m.x - t.X, top: m.y - t.Y, axes: l}), m.x = t.X, m.y = t.Y)
            }
        }

        function T(e) {
            if (v) {
                g && (clearTimeout(g), g = null), v = !1;
                var t = i.getPageXY(e);
                a.getPlaceholder().css("cursor", d), p ? (a.smartPan({
                    x: s.startPageX - t.X,
                    y: s.startPageY - t.Y
                }, s, l, !1, h), a.smartPan.end()) : u && (a.pan({
                    left: m.x - t.X,
                    top: m.y - t.Y,
                    axes: l
                }), m.x = 0, m.y = 0)
            }
        }

        function M(t) {
            if (a.activate(), a.getOptions().recenter.interactive) {
                var i, n = a.getTouchedAxis(t.clientX, t.clientY);
                a.recenter({axes: n[0] ? n : null}), i = n[0] ? new e.Event("re-center", {detail: {axisTouched: n[0]}}) : new e.Event("re-center", {detail: t}), a.getPlaceholder().trigger(i)
            }
        }

        function S(e) {
            return a.activate(), v && T(e), !1
        }

        a.navigationState = function (e, t) {
            var i = this.getAxes(), n = {};
            return Object.keys(i).forEach((function (e) {
                var t = i[e];
                n[e] = {
                    navigationOffset: {below: t.options.offset.below || 0, above: t.options.offset.above || 0},
                    axisMin: t.min,
                    axisMax: t.max,
                    diagMode: !1
                }
            })), n.startPageX = e || 0, n.startPageY = t || 0, n
        }, a.activate = function () {
            var e = a.getOptions();
            e.pan.active && e.zoom.active || (e.pan.active = !0, e.zoom.active = !0, a.getPlaceholder().trigger("plotactivated", [a]))
        }, a.zoomOut = function (e) {
            e || (e = {}), e.amount || (e.amount = a.getOptions().zoom.amount), e.amount = 1 / e.amount, a.zoom(e)
        }, a.zoom = function (t) {
            t || (t = {});
            var i = t.center, n = t.amount || a.getOptions().zoom.amount, o = a.width(), r = a.height(),
                s = t.axes || a.getAxes();
            i || (i = {left: o / 2, top: r / 2});
            var l = i.left / o, c = i.top / r, u = {
                x: {min: i.left - l * o / n, max: i.left + (1 - l) * o / n},
                y: {min: i.top - c * r / n, max: i.top + (1 - c) * r / n}
            };
            for (var h in s) if (s.hasOwnProperty(h)) {
                var p = s[h], d = p.options, f = u[p.direction].min, g = u[p.direction].max, m = p.options.offset;
                if ((d.axisZoom || !t.axes) && (t.axes || d.plotZoom)) {
                    if (f = e.plot.saturated.saturate(p.c2p(f)), (g = e.plot.saturated.saturate(p.c2p(g))) < f) {
                        var v = f;
                        f = g, g = v
                    }
                    if (d.zoomRange) {
                        if (g - f < d.zoomRange[0]) continue;
                        if (g - f > d.zoomRange[1]) continue
                    }
                    var x = e.plot.saturated.saturate(m.below - (p.min - f)),
                        b = e.plot.saturated.saturate(m.above - (p.max - g));
                    d.offset = {below: x, above: b}
                }
            }
            a.setupGrid(!0), a.draw(), t.preventEvent || a.getPlaceholder().trigger("plotzoom", [a, t])
        }, a.pan = function (i) {
            var n = {x: +i.left, y: +i.top};
            isNaN(n.x) && (n.x = 0), isNaN(n.y) && (n.y = 0), e.each(i.axes || a.getAxes(), (function (e, o) {
                var a = o.options, r = n[o.direction];
                if ((a.axisPan || !i.axes) && (a.plotPan || i.axes)) {
                    var s = o.p2c(a.panRange[0]) - o.p2c(o.min), l = o.p2c(a.panRange[1]) - o.p2c(o.max);
                    if (void 0 !== a.panRange[0] && l <= r && (r = l), void 0 !== a.panRange[1] && r <= s && (r = s), 0 !== r) {
                        var c = t.saturate(o.c2p(o.p2c(o.min) + r) - o.c2p(o.p2c(o.min))),
                            u = t.saturate(o.c2p(o.p2c(o.max) + r) - o.c2p(o.p2c(o.max)));
                        isFinite(c) || (c = 0), isFinite(u) || (u = 0), a.offset = {
                            below: t.saturate(c + (a.offset.below || 0)),
                            above: t.saturate(u + (a.offset.above || 0))
                        }
                    }
                }
            })), a.setupGrid(!0), a.draw(), i.preventEvent || a.getPlaceholder().trigger("plotpan", [a, i])
        }, a.recenter = function (t) {
            e.each(t.axes || a.getAxes(), (function (e, i) {
                t.axes ? "x" === this.direction ? i.options.offset = {below: 0} : "y" === this.direction && (i.options.offset = {above: 0}) : i.options.offset = {
                    below: 0,
                    above: 0
                }
            })), a.setupGrid(!0), a.draw()
        };
        var P = null, C = {x: 0, y: 0};
        a.smartPan = function (e, i, o, r, s) {
            var l, c, u, h, p, d, g, m, v, x, b, y, w,
                k = !!s || (c = e, Math.abs(c.y) < n && Math.abs(c.x) >= n || Math.abs(c.x) < n && Math.abs(c.y) >= n),
                T = a.getAxes();
            e = s ? function (e) {
                switch (!P && Math.max(Math.abs(e.x), Math.abs(e.y)) >= n && (P = Math.abs(e.x) < Math.abs(e.y) ? "y" : "x"), P) {
                    case"x":
                        return {x: e.x, y: 0};
                    case"y":
                        return {x: 0, y: e.y};
                    default:
                        return {x: 0, y: 0}
                }
            }(e) : (u = e, Math.abs(u.x) < n && Math.abs(u.y) >= n ? {
                x: 0,
                y: u.y
            } : Math.abs(u.y) < n && Math.abs(u.x) >= n ? {
                x: u.x,
                y: 0
            } : u), h = e, 0 < Math.abs(h.x) && 0 < Math.abs(h.y) && (i.diagMode = !0), k && !0 === i.diagMode && (i.diagMode = !1, p = T, d = i, g = e, Object.keys(p).forEach((function (e) {
                m = p[e], 0 === g[m.direction] && (m.options.offset.below = d[e].navigationOffset.below, m.options.offset.above = d[e].navigationOffset.above)
            }))), f = k ? {
                start: {
                    x: i.startPageX - a.offset().left + a.getPlotOffset().left,
                    y: i.startPageY - a.offset().top + a.getPlotOffset().top
                },
                end: {
                    x: i.startPageX - e.x - a.offset().left + a.getPlotOffset().left,
                    y: i.startPageY - e.y - a.offset().top + a.getPlotOffset().top
                }
            } : {
                start: {
                    x: i.startPageX - a.offset().left + a.getPlotOffset().left,
                    y: i.startPageY - a.offset().top + a.getPlotOffset().top
                }, end: !1
            }, isNaN(e.x) && (e.x = 0), isNaN(e.y) && (e.y = 0), o && (T = o), Object.keys(T).forEach((function (i) {
                if (v = T[i], x = v.min, b = v.max, l = v.options, w = e[v.direction], y = C[v.direction], (l.axisPan || !o) && (o || l.plotPan)) {
                    var n = y + v.p2c(l.panRange[0]) - v.p2c(x), a = y + v.p2c(l.panRange[1]) - v.p2c(b);
                    if (void 0 !== l.panRange[0] && a <= w && (w = a), void 0 !== l.panRange[1] && w <= n && (w = n), 0 !== w) {
                        var r = t.saturate(v.c2p(v.p2c(x) - (y - w)) - v.c2p(v.p2c(x))),
                            s = t.saturate(v.c2p(v.p2c(b) - (y - w)) - v.c2p(v.p2c(b)));
                        isFinite(r) || (r = 0), isFinite(s) || (s = 0), v.options.offset.below = t.saturate(r + (v.options.offset.below || 0)), v.options.offset.above = t.saturate(s + (v.options.offset.above || 0))
                    }
                }
            })), C = e, a.setupGrid(!0), a.draw(), r || a.getPlaceholder().trigger("plotpan", [a, e, o, i])
        }, a.smartPan.end = function () {
            P = f = null, C = {x: 0, y: 0}, a.triggerRedrawOverlay()
        }, a.getTouchedAxis = function (e, t) {
            var i = a.getPlaceholder().offset();
            return i.left = e - i.left, i.top = t - i.top, a.getXAxes().concat(a.getYAxes()).filter((function (e) {
                var t = e.box;
                if (void 0 !== t) return i.left > t.left && i.left < t.left + t.width && i.top > t.top && i.top < t.top + t.height
            }))
        }, a.hooks.drawOverlay.push((function (e, t) {
            if (f) {
                t.strokeStyle = "rgba(96, 160, 208, 0.7)", t.lineWidth = 2, t.lineJoin = "round";
                var i, n, a = Math.round(f.start.x), r = Math.round(f.start.y);
                if (l ? "x" === l[0].direction ? (n = Math.round(f.start.y), i = Math.round(f.end.x)) : "y" === l[0].direction && (i = Math.round(f.start.x), n = Math.round(f.end.y)) : (i = Math.round(f.end.x), n = Math.round(f.end.y)), t.beginPath(), !1 === f.end) t.moveTo(a, r - o), t.lineTo(a, r + o), t.moveTo(a + o, r), t.lineTo(a - o, r); else {
                    var s = r === n;
                    t.moveTo(a - (s ? 0 : o), r - (s ? o : 0)), t.lineTo(a + (s ? 0 : o), r + (s ? o : 0)), t.moveTo(a, r), t.lineTo(i, n), t.moveTo(i - (s ? 0 : o), n - (s ? o : 0)), t.lineTo(i + (s ? 0 : o), n + (s ? o : 0))
                }
                t.stroke()
            }
        })), a.hooks.bindEvents.push((function (e, t) {
            var i = e.getOptions();
            i.zoom.interactive && t.mousewheel(x), i.pan.interactive && (e.addEventHandler("dragstart", w, t, 0), e.addEventHandler("drag", k, t, 0), e.addEventHandler("dragend", T, t, 0), t.bind("mousedown", b), t.bind("mouseup", y)), t.dblclick(M), t.click(S)
        })), a.hooks.shutdown.push((function (e, t) {
            t.unbind("mousewheel", x), t.unbind("mousedown", b), t.unbind("mouseup", y), t.unbind("dragstart", w), t.unbind("drag", k), t.unbind("dragend", T), t.unbind("dblclick", M), t.unbind("click", S), g && clearTimeout(g)
        }))
    }

    e.plot.plugins.push({
        init: function (e) {
            e.hooks.processOptions.push(a)
        },
        options: {
            zoom: {interactive: !1, active: !1, amount: 1.5},
            pan: {interactive: !1, active: !1, cursor: "move", frameRate: 60, mode: "smart"},
            recenter: {interactive: !0},
            xaxis: {
                axisZoom: !0,
                plotZoom: !0,
                axisPan: !0,
                plotPan: !0,
                panRange: [void 0, void 0],
                zoomRange: [void 0, void 0]
            },
            yaxis: {
                axisZoom: !0,
                plotZoom: !0,
                axisPan: !0,
                plotPan: !0,
                panRange: [void 0, void 0],
                zoomRange: [void 0, void 0]
            }
        },
        name: "navigate",
        version: "1.3"
    })
}(jQuery), jQuery.plot.plugins.push({
    init: function (e) {
        e.hooks.processRawData.push((function (e, t, i, n) {
            if (null != t.fillBetween) {
                var o = n.format;
                o || ((o = []).push({
                    x: !0,
                    number: !0,
                    computeRange: "none" !== t.xaxis.options.autoScale,
                    required: !0
                }), o.push({
                    y: !0,
                    number: !0,
                    computeRange: "none" !== t.yaxis.options.autoScale,
                    required: !0
                }), void 0 !== t.fillBetween && "" !== t.fillBetween && function (t) {
                    for (var i = e.getData(), n = 0; n < i.length; n++) if (i[n].id === t) return !0;
                    return !1
                }(t.fillBetween) && t.fillBetween !== t.id && o.push({
                    x: !1,
                    y: !0,
                    number: !0,
                    required: !1,
                    computeRange: "none" !== t.yaxis.options.autoScale,
                    defaultValue: 0
                }), n.format = o)
            }
        })), e.hooks.processDatapoints.push((function (e, t, i) {
            if (null != t.fillBetween) {
                var n = function (e, t) {
                    var i;
                    for (i = 0; i < t.length; ++i) if (t[i].id === e.fillBetween) return t[i];
                    return "number" == typeof e.fillBetween ? e.fillBetween < 0 || e.fillBetween >= t.length ? null : t[e.fillBetween] : null
                }(t, e.getData());
                if (n) {
                    for (var o, a, r, s, l, c, u, h, p = i.pointsize, d = i.points, f = n.datapoints.pointsize, g = n.datapoints.points, m = [], v = t.lines.show, x = 2 < p && i.format[2].y, b = v && t.lines.steps, y = !0, w = 0, k = 0; !(w >= d.length);) {
                        if (u = m.length, null == d[w]) {
                            for (h = 0; h < p; ++h) m.push(d[w + h]);
                            w += p
                        } else if (k >= g.length) {
                            if (!v) for (h = 0; h < p; ++h) m.push(d[w + h]);
                            w += p
                        } else if (null == g[k]) {
                            for (h = 0; h < p; ++h) m.push(null);
                            y = !0, k += f
                        } else {
                            if (o = d[w], a = d[w + 1], s = g[k], l = g[k + 1], c = 0, o === s) {
                                for (h = 0; h < p; ++h) m.push(d[w + h]);
                                c = l, w += p, k += f
                            } else if (s < o) {
                                if (v && 0 < w && null != d[w - p]) {
                                    for (r = a + (d[w - p + 1] - a) * (s - o) / (d[w - p] - o), m.push(s), m.push(r), h = 2; h < p; ++h) m.push(d[w + h]);
                                    c = l
                                }
                                k += f
                            } else {
                                if (y && v) {
                                    w += p;
                                    continue
                                }
                                for (h = 0; h < p; ++h) m.push(d[w + h]);
                                v && 0 < k && null != g[k - f] && (c = l + (g[k - f + 1] - l) * (o - s) / (g[k - f] - s)), w += p
                            }
                            y = !1, u !== m.length && x && (m[u + 2] = c)
                        }
                        if (b && u !== m.length && 0 < u && null !== m[u] && m[u] !== m[u - p] && m[u + 1] !== m[u - p + 1]) {
                            for (h = 0; h < p; ++h) m[u + p + h] = m[u + h];
                            m[u + 1] = m[u - p + 1]
                        }
                    }
                    i.points = m
                }
            }
        }))
    }, options: {series: {fillBetween: null}}, name: "fillbetween", version: "1.0"
}), function (e) {
    function t(e, t, i, n) {
        var o = "categories" === t.xaxis.options.mode, a = "categories" === t.yaxis.options.mode;
        if (o || a) {
            var r = n.format;
            if (!r) {
                var s = t;
                if ((r = []).push({x: !0, number: !0, required: !0, computeRange: !0}), r.push({
                    y: !0,
                    number: !0,
                    required: !0,
                    computeRange: !0
                }), s.bars.show || s.lines.show && s.lines.fill) {
                    var l = !!(s.bars.show && s.bars.zero || s.lines.show && s.lines.zero);
                    r.push({
                        y: !0,
                        number: !0,
                        required: !1,
                        defaultValue: 0,
                        computeRange: l
                    }), s.bars.horizontal && (delete r[r.length - 1].y, r[r.length - 1].x = !0)
                }
                n.format = r
            }
            for (var c = 0; c < r.length; ++c) r[c].x && o && (r[c].number = !1), r[c].y && a && (r[c].number = !1, r[c].computeRange = !1)
        }
    }

    function i(e) {
        var t = [];
        for (var i in e.categories) {
            var n = e.categories[i];
            n >= e.min && n <= e.max && t.push([n, i])
        }
        return t.sort((function (e, t) {
            return e[0] - t[0]
        })), t
    }

    function n(t, n, o) {
        if ("categories" === t[n].options.mode) {
            if (!t[n].categories) {
                var a = {}, r = t[n].options.categories || {};
                if (e.isArray(r)) for (var s = 0; s < r.length; ++s) a[r[s]] = s; else for (var l in r) a[l] = r[l];
                t[n].categories = a
            }
            t[n].options.ticks || (t[n].options.ticks = i), function (e, t, i) {
                for (var n = e.points, o = e.pointsize, a = e.format, r = t.charAt(0), s = function (e) {
                    var t = -1;
                    for (var i in e) e[i] > t && (t = e[i]);
                    return t + 1
                }(i), l = 0; l < n.length; l += o) if (null != n[l]) for (var c = 0; c < o; ++c) {
                    var u = n[l + c];
                    null != u && a[c][r] && (u in i || (i[u] = s, ++s), n[l + c] = i[u])
                }
            }(o, n, t[n].categories)
        }
    }

    function o(e, t, i) {
        n(t, "xaxis", i), n(t, "yaxis", i)
    }

    e.plot.plugins.push({
        init: function (e) {
            e.hooks.processRawData.push(t), e.hooks.processDatapoints.push(o)
        }, options: {xaxis: {categories: null}, yaxis: {categories: null}}, name: "categories", version: "1.0"
    })
}(jQuery), jQuery.plot.plugins.push({
    init: function (e) {
        e.hooks.processDatapoints.push((function (e, t, i) {
            if (null != t.stack && !1 !== t.stack) {
                var n = t.bars.show || t.lines.show && t.lines.fill,
                    o = 2 < i.pointsize && (t.bars.horizontal ? i.format[2].x : i.format[2].y);
                n && !o && function (e, t) {
                    for (var i = [], n = 0; n < t.points.length; n += 2) i.push(t.points[n]), i.push(t.points[n + 1]), i.push(0);
                    t.format.push({
                        x: e.bars.horizontal,
                        y: !e.bars.horizontal,
                        number: !0,
                        required: !1,
                        computeRange: "none" !== e.yaxis.options.autoScale,
                        defaultValue: 0
                    }), t.points = i, t.pointsize = 3
                }(t, i);
                var a = function (e, t) {
                    for (var i = null, n = 0; n < t.length && e !== t[n]; ++n) t[n].stack === e.stack && (i = t[n]);
                    return i
                }(t, e.getData());
                if (a) {
                    for (var r, s, l, c, u, h, p, d, f = i.pointsize, g = i.points, m = a.datapoints.pointsize, v = a.datapoints.points, x = [], b = t.lines.show, y = t.bars.horizontal, w = b && t.lines.steps, k = !0, T = y ? 1 : 0, M = y ? 0 : 1, S = 0, P = 0; !(S >= g.length);) {
                        if (p = x.length, null == g[S]) {
                            for (d = 0; d < f; ++d) x.push(g[S + d]);
                            S += f
                        } else if (P >= v.length) {
                            if (!b) for (d = 0; d < f; ++d) x.push(g[S + d]);
                            S += f
                        } else if (null == v[P]) {
                            for (d = 0; d < f; ++d) x.push(null);
                            k = !0, P += m
                        } else {
                            if (r = g[S + T], s = g[S + M], c = v[P + T], u = v[P + M], h = 0, r === c) {
                                for (d = 0; d < f; ++d) x.push(g[S + d]);
                                x[p + M] += u, h = u, S += f, P += m
                            } else if (c < r) {
                                if (b && 0 < S && null != g[S - f]) {
                                    for (l = s + (g[S - f + M] - s) * (c - r) / (g[S - f + T] - r), x.push(c), x.push(l + u), d = 2; d < f; ++d) x.push(g[S + d]);
                                    h = u
                                }
                                P += m
                            } else {
                                if (k && b) {
                                    S += f;
                                    continue
                                }
                                for (d = 0; d < f; ++d) x.push(g[S + d]);
                                b && 0 < P && null != v[P - m] && (h = u + (v[P - m + M] - u) * (r - c) / (v[P - m + T] - c)), x[p + M] += h, S += f
                            }
                            k = !1, p !== x.length && n && (x[p + 2] += h)
                        }
                        if (w && p !== x.length && 0 < p && null !== x[p] && x[p] !== x[p - f] && x[p + 1] !== x[p - f + 1]) {
                            for (d = 0; d < f; ++d) x[p + f + d] = x[p + d];
                            x[p + 1] = x[p - f + 1]
                        }
                    }
                    i.points = x
                }
            }
        }))
    }, options: {series: {stack: null}}, name: "stack", version: "1.2"
}), function (e) {
    var t = e.plot.uiConstants.ZOOM_DISTANCE_MARGIN;

    function i(i, c) {
        var u, h, p, d, f = {
                zoomEnable: !1,
                prevDistance: null,
                prevTapTime: 0,
                prevPanPosition: {x: 0, y: 0},
                prevTapPosition: {x: 0, y: 0}
            }, g = {
                prevTouchedAxis: "none",
                currentTouchedAxis: "none",
                touchedAxis: null,
                navigationConstraint: "unconstrained",
                initialState: null
            }, m = c.pan.interactive && "manual" === c.pan.touchMode, v = "smartLock" === c.pan.touchMode,
            x = c.pan.interactive && (v || "smart" === c.pan.touchMode);

        function b(e, t, o) {
            g.touchedAxis = function (e, t, i, n) {
                if ("pinchstart" !== t.type) return "panstart" === t.type || "pinchend" === t.type ? e.getTouchedAxis(t.detail.touches[0].pageX, t.detail.touches[0].pageY) : n.touchedAxis;
                var o = e.getTouchedAxis(t.detail.touches[0].pageX, t.detail.touches[0].pageY),
                    a = e.getTouchedAxis(t.detail.touches[1].pageX, t.detail.touches[1].pageY);
                return o.length === a.length && o.toString() === a.toString() ? o : void 0
            }(i, e, 0, g), n(g) ? g.navigationConstraint = "unconstrained" : g.navigationConstraint = "axisConstrained"
        }

        u = {
            start: function (e) {
                if (b(e), o(e, "pan", f, g), x) {
                    var t = l(e, "pan");
                    g.initialState = i.navigationState(t.x, t.y)
                }
            }, drag: function (e) {
                if (b(e), x) {
                    var t = l(e, "pan");
                    i.smartPan({
                        x: g.initialState.startPageX - t.x,
                        y: g.initialState.startPageY - t.y
                    }, g.initialState, g.touchedAxis, !1, v)
                } else m && (i.pan({
                    left: -s(e, "pan", f).x,
                    top: -s(e, "pan", f).y,
                    axes: g.touchedAxis
                }), r(e, "pan", f, g))
            }, end: function (e) {
                var t;
                b(e), x && i.smartPan.end(), t = e, f.zoomEnable && 1 === t.detail.touches.length && updateprevPanPosition(e, "pan", f, g)
            }
        }, h = {
            start: function (e) {
                var t;
                d && (clearTimeout(d), d = null), b(e), t = e, f.prevDistance = a(t), o(e, "pinch", f, g)
            }, drag: function (e) {
                d || (d = setTimeout((function () {
                    b(e), i.pan({
                        left: -s(e, "pinch", f).x,
                        top: -s(e, "pinch", f).y,
                        axes: g.touchedAxis
                    }), r(e, "pinch", f, g);
                    var n, o, c, u, h, p, m, v, x = a(e);
                    (f.zoomEnable || Math.abs(x - f.prevDistance) > t) && (o = e, c = f, u = g, h = (n = i).offset(), p = {
                        left: 0,
                        top: 0
                    }, m = a(o) / c.prevDistance, v = a(o), p.left = l(o, "pinch").x - h.left, p.top = l(o, "pinch").y - h.top, n.zoom({
                        center: p,
                        amount: m,
                        axes: u.touchedAxis
                    }), c.prevDistance = v, f.zoomEnable = !0), d = null
                }), 1e3 / 60))
            }, end: function (e) {
                d && (clearTimeout(d), d = null), b(e), f.prevDistance = null
            }
        }, p = {
            recenterPlot: function (t) {
                t && t.detail && "touchstart" === t.detail.type && function (t, i, o, a) {
                    var r, s, l, c, u;
                    (l = i, c = a, void 0 !== (u = (s = t).getTouchedAxis(l.detail.firstTouch.x, l.detail.firstTouch.y))[0] && (c.prevTouchedAxis = u[0].direction), void 0 !== (u = s.getTouchedAxis(l.detail.secondTouch.x, l.detail.secondTouch.y))[0] && (c.touchedAxis = u, c.currentTouchedAxis = u[0].direction), n(c) && (c.touchedAxis = null, c.prevTouchedAxis = "none", c.currentTouchedAxis = "none"), "x" === a.currentTouchedAxis && "x" === a.prevTouchedAxis || "y" === a.currentTouchedAxis && "y" === a.prevTouchedAxis || "none" === a.currentTouchedAxis && "none" === a.prevTouchedAxis) && (t.recenter({axes: a.touchedAxis}), r = a.touchedAxis ? new e.Event("re-center", {detail: {axisTouched: a.touchedAxis}}) : new e.Event("re-center", {detail: i}), t.getPlaceholder().trigger(r))
                }(i, t, 0, g)
            }
        }, !0 !== c.pan.enableTouch && !0 !== c.zoom.enableTouch || (i.hooks.bindEvents.push((function (e, t) {
            var i = e.getOptions();
            i.zoom.interactive && i.zoom.enableTouch && (t[0].addEventListener("pinchstart", h.start, !1), t[0].addEventListener("pinchdrag", h.drag, !1), t[0].addEventListener("pinchend", h.end, !1)), i.pan.interactive && i.pan.enableTouch && (t[0].addEventListener("panstart", u.start, !1), t[0].addEventListener("pandrag", u.drag, !1), t[0].addEventListener("panend", u.end, !1)), i.recenter.interactive && i.recenter.enableTouch && t[0].addEventListener("doubletap", p.recenterPlot, !1)
        })), i.hooks.shutdown.push((function (e, t) {
            t[0].removeEventListener("panstart", u.start), t[0].removeEventListener("pandrag", u.drag), t[0].removeEventListener("panend", u.end), t[0].removeEventListener("pinchstart", h.start), t[0].removeEventListener("pinchdrag", h.drag), t[0].removeEventListener("pinchend", h.end), t[0].removeEventListener("doubletap", p.recenterPlot)
        })))
    }

    function n(e) {
        return !e.touchedAxis || 0 === e.touchedAxis.length
    }

    function o(e, t, i, n) {
        var o, a = l(e, t);
        switch (n.navigationConstraint) {
            case"unconstrained":
                n.touchedAxis = null, i.prevTapPosition = {
                    x: i.prevPanPosition.x,
                    y: i.prevPanPosition.y
                }, i.prevPanPosition = {x: a.x, y: a.y};
                break;
            case"axisConstrained":
                o = n.touchedAxis[0].direction, n.currentTouchedAxis = o, i.prevTapPosition[o] = i.prevPanPosition[o], i.prevPanPosition[o] = a[o]
        }
    }

    function a(e) {
        var t, i, n, o, a = e.detail.touches[0], r = e.detail.touches[1];
        return t = a.pageX, i = a.pageY, n = r.pageX, o = r.pageY, Math.sqrt((t - n) * (t - n) + (i - o) * (i - o))
    }

    function r(e, t, i, n) {
        var o = l(e, t);
        switch (n.navigationConstraint) {
            case"unconstrained":
                i.prevPanPosition.x = o.x, i.prevPanPosition.y = o.y;
                break;
            case"axisConstrained":
                i.prevPanPosition[n.currentTouchedAxis] = o[n.currentTouchedAxis]
        }
    }

    function s(e, t, i) {
        var n = l(e, t);
        return {x: n.x - i.prevPanPosition.x, y: n.y - i.prevPanPosition.y}
    }

    function l(e, t) {
        return "pinch" === t ? {
            x: (e.detail.touches[0].pageX + e.detail.touches[1].pageX) / 2,
            y: (e.detail.touches[0].pageY + e.detail.touches[1].pageY) / 2
        } : {x: e.detail.touches[0].pageX, y: e.detail.touches[0].pageY}
    }

    e.plot.plugins.push({
        init: function (e) {
            e.hooks.processOptions.push(i)
        },
        options: {zoom: {enableTouch: !1}, pan: {enableTouch: !1, touchMode: "manual"}, recenter: {enableTouch: !0}},
        name: "navigateTouch",
        version: "0.3"
    })
}(jQuery), function (e) {
    var t = e.plot.browser, i = "hover";
    e.plot.plugins.push({
        init: function (n) {
            var o, a = [];

            function r(e) {
                var t = n.getOptions(), o = new CustomEvent("mouseevent");
                return o.pageX = e.detail.changedTouches[0].pageX, o.pageY = e.detail.changedTouches[0].pageY, o.clientX = e.detail.changedTouches[0].clientX, o.clientY = e.detail.changedTouches[0].clientY, t.grid.hoverable && s(o, i, 30), !1
            }

            function s(e, t, i) {
                var o = n.getData();
                if (void 0 !== e && 0 < o.length && void 0 !== o[0].xaxis.c2p && void 0 !== o[0].yaxis.c2p) {
                    var a = t + "able";
                    p("plot" + t, e, (function (e) {
                        return !1 !== o[e][a]
                    }), i)
                }
            }

            function l(e) {
                o = e, s(n.getPlaceholder()[0].lastMouseMoveEvent = e, i)
            }

            function c(e) {
                o = void 0, n.getPlaceholder()[0].lastMouseMoveEvent = void 0, p("plothover", e, (function (e) {
                    return !1
                }))
            }

            function u(e) {
                s(e, "click")
            }

            function h() {
                n.unhighlight(), n.getPlaceholder().trigger("plothovercleanup")
            }

            function p(e, i, o, r) {
                var s = n.getOptions(), l = n.offset(), c = t.getPageXY(i), u = c.X - l.left, h = c.Y - l.top,
                    p = n.c2p({left: u, top: h}), g = void 0 !== r ? r : s.grid.mouseActiveRadius;
                p.pageX = c.X, p.pageY = c.Y;
                for (var m = n.findNearbyItems(u, h, o, g), v = m[0], x = 1; x < m.length; ++x) (void 0 === v.distance || m[x].distance < v.distance) && (v = m[x]);
                if (v ? (v.pageX = parseInt(v.series.xaxis.p2c(v.datapoint[0]) + l.left, 10), v.pageY = parseInt(v.series.yaxis.p2c(v.datapoint[1]) + l.top, 10)) : v = null, s.grid.autoHighlight) {
                    for (var b = 0; b < a.length; ++b) {
                        var y = a[b];
                        (y.auto !== e || v && y.series === v.series && y.point[0] === v.datapoint[0] && y.point[1] === v.datapoint[1]) && v || f(y.series, y.point)
                    }
                    v && d(v.series, v.datapoint, e)
                }
                n.getPlaceholder().trigger(e, [p, v, m])
            }

            function d(e, t, i) {
                if ("number" == typeof e && (e = n.getData()[e]), "number" == typeof t) {
                    var o = e.datapoints.pointsize;
                    t = e.datapoints.points.slice(o * t, o * (t + 1))
                }
                var r = g(e, t);
                -1 === r ? (a.push({series: e, point: t, auto: i}), n.triggerRedrawOverlay()) : i || (a[r].auto = !1)
            }

            function f(e, t) {
                if (null == e && null == t) return a = [], void n.triggerRedrawOverlay();
                if ("number" == typeof e && (e = n.getData()[e]), "number" == typeof t) {
                    var i = e.datapoints.pointsize;
                    t = e.datapoints.points.slice(i * t, i * (t + 1))
                }
                var o = g(e, t);
                -1 !== o && (a.splice(o, 1), n.triggerRedrawOverlay())
            }

            function g(e, t) {
                for (var i = 0; i < a.length; ++i) {
                    var n = a[i];
                    if (n.series === e && n.point[0] === t[0] && n.point[1] === t[1]) return i
                }
                return -1
            }

            function m() {
                h(), s(o, i)
            }

            function v() {
                s(o, i)
            }

            function x(e, t, i) {
                var n, o, r = e.getPlotOffset();
                for (t.save(), t.translate(r.left, r.top), n = 0; n < a.length; ++n) (o = a[n]).series.bars.show ? y(o.series, o.point, t) : b(o.series, o.point, t, e);
                t.restore()
            }

            function b(t, i, n, o) {
                var a = i[0], r = i[1], s = t.xaxis, l = t.yaxis,
                    c = "string" == typeof t.highlightColor ? t.highlightColor : e.color.parse(t.color).scale("a", .5).toString();
                if (!(a < s.min || a > s.max || r < l.min || r > l.max)) {
                    var u = t.points.radius + t.points.lineWidth / 2;
                    n.lineWidth = u, n.strokeStyle = c;
                    var h = 1.5 * u;
                    a = s.p2c(a), r = l.p2c(r), n.beginPath();
                    var p = t.points.symbol;
                    "circle" === p ? n.arc(a, r, h, 0, 2 * Math.PI, !1) : "string" == typeof p && o.drawSymbol && o.drawSymbol[p] && o.drawSymbol[p](n, a, r, h, !1), n.closePath(), n.stroke()
                }
            }

            function y(t, i, n) {
                var o,
                    a = "string" == typeof t.highlightColor ? t.highlightColor : e.color.parse(t.color).scale("a", .5).toString(),
                    r = a, s = t.bars.barWidth[0] || t.bars.barWidth;
                switch (t.bars.align) {
                    case"left":
                        o = 0;
                        break;
                    case"right":
                        o = -s;
                        break;
                    default:
                        o = -s / 2
                }
                n.lineWidth = t.bars.lineWidth, n.strokeStyle = a;
                var l = t.bars.fillTowards || 0, c = l > t.yaxis.min ? Math.min(t.yaxis.max, l) : t.yaxis.min;
                e.plot.drawSeries.drawBar(i[0], i[1], i[2] || c, o, o + s, (function () {
                    return r
                }), t.xaxis, t.yaxis, n, t.bars.horizontal, t.bars.lineWidth)
            }

            n.hooks.bindEvents.push((function (e, t) {
                var i = e.getOptions();
                (i.grid.hoverable || i.grid.clickable) && (t[0].addEventListener("touchevent", h, !1), t[0].addEventListener("tap", r, !1)), i.grid.clickable && t.bind("click", u), i.grid.hoverable && (t.bind("mousemove", l), t.bind("mouseleave", c))
            })), n.hooks.shutdown.push((function (e, t) {
                t[0].removeEventListener("tap", r), t[0].removeEventListener("touchevent", h), t.unbind("mousemove", l), t.unbind("mouseleave", c), t.unbind("click", u), a = []
            })), n.hooks.processOptions.push((function (e, t) {
                e.highlight = d, e.unhighlight = f, (t.grid.hoverable || t.grid.clickable) && (e.hooks.drawOverlay.push(x), e.hooks.processDatapoints.push(m), e.hooks.setupGrid.push(v)), o = e.getPlaceholder()[0].lastMouseMoveEvent
            }))
        }, options: {grid: {hoverable: !1, clickable: !1}}, name: "hover", version: "0.1"
    })
}(jQuery), function (e) {
    function t(e, t) {
        var i, n = {
            twoTouches: !1,
            currentTapStart: {x: 0, y: 0},
            currentTapEnd: {x: 0, y: 0},
            prevTap: {x: 0, y: 0},
            currentTap: {x: 0, y: 0},
            interceptedLongTap: !1,
            isUnsupportedGesture: !1,
            prevTapTime: null,
            tapStartTime: null,
            longTapTriggerId: null
        };

        function o(t) {
            var o = e.getOptions();
            (o.pan.active || o.zoom.active) && (3 <= t.touches.length ? n.isUnsupportedGesture = !0 : n.isUnsupportedGesture = !1, i.dispatchEvent(new CustomEvent("touchevent", {detail: t})), g(t) ? a(t, "pinch") : (a(t, "pan"), f(t) || (function (e) {
                var t = (new Date).getTime(), i = t - n.prevTapTime;
                return 0 <= i && i < 500 && d(n.prevTap.x, n.prevTap.y, n.currentTap.x, n.currentTap.y) < 20 ? (e.firstTouch = n.prevTap, e.secondTouch = n.currentTap, !0) : (n.prevTapTime = t, !1)
            }(t) && a(t, "doubleTap"), a(t, "tap"), a(t, "longTap"))))
        }

        function a(e, t) {
            switch (t) {
                case"pan":
                    r[e.type](e);
                    break;
                case"pinch":
                    s[e.type](e);
                    break;
                case"doubleTap":
                    l.onDoubleTap(e);
                    break;
                case"longTap":
                    c[e.type](e);
                    break;
                case"tap":
                    u[e.type](e)
            }
        }

        var r = {
            touchstart: function (e) {
                var t;
                n.prevTap = {
                    x: n.currentTap.x,
                    y: n.currentTap.y
                }, h(e), t = e, n.tapStartTime = (new Date).getTime(), n.interceptedLongTap = !1, n.currentTapStart = {
                    x: t.touches[0].pageX,
                    y: t.touches[0].pageY
                }, n.currentTapEnd = {
                    x: t.touches[0].pageX,
                    y: t.touches[0].pageY
                }, i.dispatchEvent(new CustomEvent("panstart", {detail: e}))
            }, touchmove: function (e) {
                var t;
                p(e), h(e), t = e, n.currentTapEnd = {
                    x: t.touches[0].pageX,
                    y: t.touches[0].pageY
                }, n.isUnsupportedGesture || i.dispatchEvent(new CustomEvent("pandrag", {detail: e}))
            }, touchend: function (e) {
                var t;
                p(e), f(e) ? (i.dispatchEvent(new CustomEvent("pinchend", {detail: e})), i.dispatchEvent(new CustomEvent("panstart", {detail: e}))) : (t = e).touches && 0 === t.touches.length && i.dispatchEvent(new CustomEvent("panend", {detail: e}))
            }
        }, s = {
            touchstart: function (e) {
                i.dispatchEvent(new CustomEvent("pinchstart", {detail: e}))
            }, touchmove: function (e) {
                p(e), n.twoTouches = g(e), n.isUnsupportedGesture || i.dispatchEvent(new CustomEvent("pinchdrag", {detail: e}))
            }, touchend: function (e) {
                p(e)
            }
        }, l = {
            onDoubleTap: function (e) {
                p(e), i.dispatchEvent(new CustomEvent("doubletap", {detail: e}))
            }
        }, c = {
            touchstart: function (e) {
                c.waitForLongTap(e)
            }, touchmove: function (e) {
            }, touchend: function (e) {
                n.longTapTriggerId && (clearTimeout(n.longTapTriggerId), n.longTapTriggerId = null)
            }, isLongTap: function (e) {
                return 1500 <= (new Date).getTime() - n.tapStartTime && !n.interceptedLongTap && d(n.currentTapStart.x, n.currentTapStart.y, n.currentTapEnd.x, n.currentTapEnd.y) < 20 && (n.interceptedLongTap = !0)
            }, waitForLongTap: function (e) {
                n.longTapTriggerId || (n.longTapTriggerId = setTimeout((function () {
                    c.isLongTap(e) && i.dispatchEvent(new CustomEvent("longtap", {detail: e})), n.longTapTriggerId = null
                }), 1500))
            }
        }, u = {
            touchstart: function (e) {
                n.tapStartTime = (new Date).getTime()
            }, touchmove: function (e) {
            }, touchend: function (e) {
                u.isTap(e) && (i.dispatchEvent(new CustomEvent("tap", {detail: e})), p(e))
            }, isTap: function (e) {
                return (new Date).getTime() - n.tapStartTime <= 125 && d(n.currentTapStart.x, n.currentTapStart.y, n.currentTapEnd.x, n.currentTapEnd.y) < 20
            }
        };

        function h(e) {
            n.currentTap = {x: e.touches[0].pageX, y: e.touches[0].pageY}
        }

        function p(t) {
            n.isUnsupportedGesture || (t.preventDefault(), e.getOptions().propagateSupportedGesture || t.stopPropagation())
        }

        function d(e, t, i, n) {
            return Math.sqrt((e - i) * (e - i) + (t - n) * (t - n))
        }

        function f(e) {
            return n.twoTouches && 1 === e.touches.length
        }

        function g(t) {
            return !!(t.touches && 2 <= t.touches.length && t.touches[0].target === e.getEventHolder() && t.touches[1].target === e.getEventHolder())
        }

        (!0 === t.pan.enableTouch || t.zoom.enableTouch) && (e.hooks.bindEvents.push((function (e, t) {
            i = t[0], t[0].addEventListener("touchstart", o, !1), t[0].addEventListener("touchmove", o, !1), t[0].addEventListener("touchend", o, !1)
        })), e.hooks.shutdown.push((function (e, t) {
            t[0].removeEventListener("touchstart", o), t[0].removeEventListener("touchmove", o), t[0].removeEventListener("touchend", o), n.longTapTriggerId && (clearTimeout(n.longTapTriggerId), n.longTapTriggerId = null)
        })))
    }

    jQuery.plot.plugins.push({
        init: function (e) {
            e.hooks.processOptions.push(t)
        }, options: {propagateSupportedGesture: !1}, name: "navigateTouch", version: "0.3"
    })
}(), function (e) {
    var t = e.plot.saturated.floorInBase, i = function (e, t) {
        var i = new e(t), n = i.setTime.bind(i);
        i.update = function (e) {
            e = Math.round(1e3 * e) / 1e3, n(e), this.microseconds = 1e3 * (e - Math.floor(e))
        };
        var o = i.getTime.bind(i);
        return i.getTime = function () {
            return o() + this.microseconds / 1e3
        }, i.setTime = function (e) {
            this.update(e)
        }, i.getMicroseconds = function () {
            return this.microseconds
        }, i.setMicroseconds = function (e) {
            var t = o() + e / 1e3;
            this.update(t)
        }, i.setUTCMicroseconds = function (e) {
            this.setMicroseconds(e)
        }, i.getUTCMicroseconds = function () {
            return this.getMicroseconds()
        }, i.microseconds = null, i.microEpoch = null, i.update(t), i
    };

    function n(e, t, i, n) {
        if ("function" == typeof e.strftime) return e.strftime(t);
        var o, a = function (e, t) {
            return t = "" + (null == t ? "0" : t), 1 === (e = "" + e).length ? t + e : e
        }, r = function (e, t, i) {
            var n, o = 1e3 * e + t;
            if (i < 6 && 0 < i) {
                var a = parseFloat("1e" + (i - 6));
                n = ("00000" + (o = Math.round(Math.round(o * a) / a))).slice(-6, -(6 - i))
            } else n = ("00000" + (o = Math.round(o))).slice(-6);
            return n
        }, s = [], l = !1, c = e.getHours(), u = c < 12;
        i || (i = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]), n || (n = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]), o = 12 < c ? c - 12 : 0 === c ? 12 : c;
        for (var h = -1, p = 0; p < t.length; ++p) {
            var d = t.charAt(p);
            if (!isNaN(Number(d)) && 0 < Number(d)) h = Number(d); else if (l) {
                switch (d) {
                    case"a":
                        d = "" + n[e.getDay()];
                        break;
                    case"b":
                        d = "" + i[e.getMonth()];
                        break;
                    case"d":
                        d = a(e.getDate());
                        break;
                    case"e":
                        d = a(e.getDate(), " ");
                        break;
                    case"h":
                    case"H":
                        d = a(c);
                        break;
                    case"I":
                        d = a(o);
                        break;
                    case"l":
                        d = a(o, " ");
                        break;
                    case"m":
                        d = a(e.getMonth() + 1);
                        break;
                    case"M":
                        d = a(e.getMinutes());
                        break;
                    case"q":
                        d = "" + (Math.floor(e.getMonth() / 3) + 1);
                        break;
                    case"S":
                        d = a(e.getSeconds());
                        break;
                    case"s":
                        d = "" + r(e.getMilliseconds(), e.getMicroseconds(), h);
                        break;
                    case"y":
                        d = a(e.getFullYear() % 100);
                        break;
                    case"Y":
                        d = "" + e.getFullYear();
                        break;
                    case"p":
                        d = u ? "am" : "pm";
                        break;
                    case"P":
                        d = u ? "AM" : "PM";
                        break;
                    case"w":
                        d = "" + e.getDay()
                }
                s.push(d), l = !1
            } else "%" === d ? l = !0 : s.push(d)
        }
        return s.join("")
    }

    function o(e) {
        function t(e, t, i, n) {
            e[t] = function () {
                return i[n].apply(i, arguments)
            }
        }

        var i = {date: e};
        void 0 !== e.strftime && t(i, "strftime", e, "strftime"), t(i, "getTime", e, "getTime"), t(i, "setTime", e, "setTime");
        for (var n = ["Date", "Day", "FullYear", "Hours", "Minutes", "Month", "Seconds", "Milliseconds", "Microseconds"], o = 0; o < n.length; o++) t(i, "get" + n[o], e, "getUTC" + n[o]), t(i, "set" + n[o], e, "setUTC" + n[o]);
        return i
    }

    function a(e, t) {
        var n = 864e13;
        if (t && "seconds" === t.timeBase ? e *= 1e3 : "microseconds" === t.timeBase && (e /= 1e3), n < e ? e = n : e < -n && (e = -n), "browser" === t.timezone) return i(Date, e);
        if (t.timezone && "utc" !== t.timezone) {
            if ("undefined" == typeof timezoneJS || void 0 === timezoneJS.Date) return o(i(Date, e));
            var a = i(timezoneJS.Date, e);
            return a.setTimezone(t.timezone), a.setTime(e), a
        }
        return o(i(Date, e))
    }

    var r = {
            microsecond: 1e-6,
            millisecond: .001,
            second: 1,
            minute: 60,
            hour: 3600,
            day: 86400,
            month: 2592e3,
            quarter: 7776e3,
            year: 525949.2 * 60
        }, s = {
            microsecond: .001,
            millisecond: 1,
            second: 1e3,
            minute: 6e4,
            hour: 36e5,
            day: 864e5,
            month: 2592e6,
            quarter: 7776e6,
            year: 525949.2 * 60 * 1e3
        }, l = {
            microsecond: 1,
            millisecond: 1e3,
            second: 1e6,
            minute: 6e7,
            hour: 36e8,
            day: 864e8,
            month: 2592e9,
            quarter: 7776e9,
            year: 31556951999999.996
        },
        c = [[1, "microsecond"], [2, "microsecond"], [5, "microsecond"], [10, "microsecond"], [25, "microsecond"], [50, "microsecond"], [100, "microsecond"], [250, "microsecond"], [500, "microsecond"], [1, "millisecond"], [2, "millisecond"], [5, "millisecond"], [10, "millisecond"], [25, "millisecond"], [50, "millisecond"], [100, "millisecond"], [250, "millisecond"], [500, "millisecond"], [1, "second"], [2, "second"], [5, "second"], [10, "second"], [30, "second"], [1, "minute"], [2, "minute"], [5, "minute"], [10, "minute"], [30, "minute"], [1, "hour"], [2, "hour"], [4, "hour"], [8, "hour"], [12, "hour"], [1, "day"], [2, "day"], [3, "day"], [.25, "month"], [.5, "month"], [1, "month"], [2, "month"]],
        u = c.concat([[3, "month"], [6, "month"], [1, "year"]]),
        h = c.concat([[1, "quarter"], [2, "quarter"], [1, "year"]]);

    function p(e) {
        var i, n = e.options, o = [], c = a(e.min, n), p = 0,
            d = n.tickSize && "quarter" === n.tickSize[1] || n.minTickSize && "quarter" === n.minTickSize[1] ? h : u;
        i = "seconds" === n.timeBase ? r : "microseconds" === n.timeBase ? l : s, null !== n.minTickSize && void 0 !== n.minTickSize && (p = "number" == typeof n.tickSize ? n.tickSize : n.minTickSize[0] * i[n.minTickSize[1]]);
        for (var f = 0; f < d.length - 1 && !(e.delta < (d[f][0] * i[d[f][1]] + d[f + 1][0] * i[d[f + 1][1]]) / 2 && d[f][0] * i[d[f][1]] >= p); ++f) ;
        var g = d[f][0], m = d[f][1];
        if ("year" === m) {
            if (null !== n.minTickSize && void 0 !== n.minTickSize && "year" === n.minTickSize[1]) g = Math.floor(n.minTickSize[0]); else {
                var v = parseFloat("1e" + Math.floor(Math.log(e.delta / i.year) / Math.LN10)), x = e.delta / i.year / v;
                g = x < 1.5 ? 1 : x < 3 ? 2 : x < 7.5 ? 5 : 10, g *= v
            }
            g < 1 && (g = 1)
        }
        e.tickSize = n.tickSize || [g, m];
        var b = e.tickSize[0], y = b * i[m = e.tickSize[1]];
        "microsecond" === m ? c.setMicroseconds(t(c.getMicroseconds(), b)) : "millisecond" === m ? c.setMilliseconds(t(c.getMilliseconds(), b)) : "second" === m ? c.setSeconds(t(c.getSeconds(), b)) : "minute" === m ? c.setMinutes(t(c.getMinutes(), b)) : "hour" === m ? c.setHours(t(c.getHours(), b)) : "month" === m ? c.setMonth(t(c.getMonth(), b)) : "quarter" === m ? c.setMonth(3 * t(c.getMonth() / 3, b)) : "year" === m && c.setFullYear(t(c.getFullYear(), b)), y >= i.millisecond && c.setMicroseconds(0), y >= i.second && c.setMilliseconds(0), y >= i.minute && c.setSeconds(0), y >= i.hour && c.setMinutes(0), y >= i.day && c.setHours(0), y >= 4 * i.day && c.setDate(1), y >= 2 * i.month && c.setMonth(t(c.getMonth(), 3)), y >= 2 * i.quarter && c.setMonth(t(c.getMonth(), 6)), y >= i.year && c.setMonth(0);
        var w, k, T = 0, M = Number.NaN;
        do {
            if (k = M, w = c.getTime(), M = n && "seconds" === n.timeBase ? w / 1e3 : n && "microseconds" === n.timeBase ? 1e3 * w : w, o.push(M), "month" === m || "quarter" === m) if (b < 1) {
                c.setDate(1);
                var S = c.getTime();
                c.setMonth(c.getMonth() + ("quarter" === m ? 3 : 1));
                var P = c.getTime();
                c.setTime(M + T * i.hour + (P - S) * b), T = c.getHours(), c.setHours(0)
            } else c.setMonth(c.getMonth() + b * ("quarter" === m ? 3 : 1)); else "year" === m ? c.setFullYear(c.getFullYear() + b) : "seconds" === n.timeBase ? c.setTime(1e3 * (M + y)) : "microseconds" === n.timeBase ? c.setTime((M + y) / 1e3) : c.setTime(M + y)
        } while (M < e.max && M !== k);
        return o
    }

    e.plot.plugins.push({
        init: function (t) {
            t.hooks.processOptions.push((function (t) {
                e.each(t.getAxes(), (function (e, t) {
                    var i = t.options;
                    if ("time" === i.mode) {
                        if (t.tickGenerator = p, "tickFormatter" in i && "function" == typeof i.tickFormatter) return;
                        t.tickFormatter = function (e, t) {
                            var o = a(e, t.options);
                            if (null != i.timeformat) return n(o, i.timeformat, i.monthNames, i.dayNames);
                            var c,
                                u = t.options.tickSize && "quarter" === t.options.tickSize[1] || t.options.minTickSize && "quarter" === t.options.minTickSize[1];
                            c = "seconds" === i.timeBase ? r : "microseconds" === i.timeBase ? l : s;
                            var h, p, d = t.tickSize[0] * c[t.tickSize[1]], f = t.max - t.min,
                                g = i.twelveHourClock ? " %p" : "", m = i.twelveHourClock ? "%I" : "%H";
                            if (h = "seconds" === i.timeBase ? 1 : "microseconds" === i.timeBase ? 1e6 : 1e3, d < c.second) {
                                var v = -Math.floor(Math.log10(d / h));
                                -1 < String(d).indexOf("25") && v++, p = "%S.%" + v + "s"
                            } else p = d < c.minute ? m + ":%M:%S" + g : d < c.day ? f < 2 * c.day ? m + ":%M" + g : "%b %d " + m + ":%M" + g : d < c.month ? "%b %d" : u && d < c.quarter || !u && d < c.year ? f < c.year ? "%b" : "%b %Y" : u && d < c.year ? f < c.year ? "Q%q" : "Q%q %Y" : "%Y";
                            return n(o, p, i.monthNames, i.dayNames)
                        }
                    }
                }))
            }))
        },
        options: {
            xaxis: {timezone: null, timeformat: null, twelveHourClock: !1, monthNames: null, timeBase: "seconds"},
            yaxis: {timeBase: "seconds"}
        },
        name: "time",
        version: "1.0"
    }), e.plot.formatDate = n, e.plot.dateGenerator = a, e.plot.dateTickGenerator = p, e.plot.makeUtcWrapper = o
}(jQuery), function (e) {
    function t(e, t, i, n, o, a) {
        this.axisName = e, this.position = t, this.padding = i, this.placeholder = n, this.axisLabel = o, this.surface = a, this.width = 0, this.height = 0, this.elem = null
    }

    t.prototype.calculateSize = function () {
        var e = this.axisName + "Label", t = e + "Layer", i = e + " axisLabels",
            n = this.surface.getTextInfo(t, this.axisLabel, i);
        this.labelWidth = n.width, this.labelHeight = n.height, "left" === this.position || "right" === this.position ? (this.width = this.labelHeight + this.padding, this.height = 0) : (this.width = 0, this.height = this.labelHeight + this.padding)
    }, t.prototype.transforms = function (e, t, i, n) {
        var o, a, r = [];
        if (0 === t && 0 === i || ((o = n.createSVGTransform()).setTranslate(t, i), r.push(o)), 0 !== e) {
            a = n.createSVGTransform();
            var s = Math.round(this.labelWidth / 2);
            a.setRotate(e, s, 0), r.push(a)
        }
        return r
    }, t.prototype.calculateOffsets = function (e) {
        var t = {x: 0, y: 0, degrees: 0};
        return "bottom" === this.position ? (t.x = e.left + e.width / 2 - this.labelWidth / 2, t.y = e.top + e.height - this.labelHeight) : "top" === this.position ? (t.x = e.left + e.width / 2 - this.labelWidth / 2, t.y = e.top) : "left" === this.position ? (t.degrees = -90, t.x = e.left - this.labelWidth / 2, t.y = e.height / 2 + e.top) : "right" === this.position && (t.degrees = 90, t.x = e.left + e.width - this.labelWidth / 2, t.y = e.height / 2 + e.top), t.x = Math.round(t.x), t.y = Math.round(t.y), t
    }, t.prototype.cleanup = function () {
        var e = this.axisName + "Label", t = e + "Layer", i = e + " axisLabels";
        this.surface.removeText(t, 0, 0, this.axisLabel, i)
    }, t.prototype.draw = function (e) {
        var t = this.axisName + "Label", i = t + "Layer", n = t + " axisLabels", o = this.calculateOffsets(e),
            a = {position: "absolute", bottom: "", right: "", display: "inline-block", "white-space": "nowrap"},
            r = this.surface.getSVGLayer(i), s = this.transforms(o.degrees, o.x, o.y, r.parentNode);
        this.surface.addText(i, 0, 0, this.axisLabel, n, void 0, void 0, void 0, void 0, s), this.surface.render(), Object.keys(a).forEach((function (e) {
            r.style[e] = a[e]
        }))
    }, e.plot.plugins.push({
        init: function (i) {
            i.hooks.processOptions.push((function (i, n) {
                if (n.axisLabels.show) {
                    var o = {};
                    i.hooks.axisReserveSpace.push((function (e, i) {
                        var n = i.options, a = i.direction + i.n;
                        if (i.labelHeight += i.boxPosition.centerY, i.labelWidth += i.boxPosition.centerX, n && n.axisLabel && i.show) {
                            var r = void 0 === n.axisLabelPadding ? 2 : n.axisLabelPadding, s = o[a];
                            s || (s = new t(a, n.position, r, e.getPlaceholder()[0], n.axisLabel, e.getSurface()), o[a] = s), s.calculateSize(), i.labelHeight += s.height, i.labelWidth += s.width
                        }
                    })), i.hooks.draw.push((function (t, i) {
                        e.each(t.getAxes(), (function (e, t) {
                            var i = t.options;
                            if (i && i.axisLabel && t.show) {
                                var n = t.direction + t.n;
                                o[n].draw(t.box)
                            }
                        }))
                    })), i.hooks.shutdown.push((function (e, t) {
                        for (var i in o) o[i].cleanup()
                    }))
                }
            }))
        }, options: {axisLabels: {show: !0}}, name: "axisLabels", version: "3.0"
    })
}(jQuery), function (e) {
    e.plot.plugins.push({
        init: function (t) {
            var i = {first: {x: -1, y: -1}, second: {x: -1, y: -1}, show: !1, currentMode: "xy", active: !1},
                n = e.plot.uiConstants.SNAPPING_CONSTANT, o = {};

            function a(e) {
                i.active && (d(e), t.getPlaceholder().trigger("plotselecting", [l()]))
            }

            function r(e) {
                var n = t.getOptions();
                1 === e.which && null !== n.selection.mode && (i.currentMode = "xy", document.body.focus(), void 0 !== document.onselectstart && null == o.onselectstart && (o.onselectstart = document.onselectstart, document.onselectstart = function () {
                    return !1
                }), void 0 !== document.ondrag && null == o.ondrag && (o.ondrag = document.ondrag, document.ondrag = function () {
                    return !1
                }), p(i.first, e), i.active = !0)
            }

            function s(e) {
                return void 0 !== document.onselectstart && (document.onselectstart = o.onselectstart), void 0 !== document.ondrag && (document.ondrag = o.ondrag), i.active = !1, d(e), m() ? c() : (t.getPlaceholder().trigger("plotunselected", []), t.getPlaceholder().trigger("plotselecting", [null])), !1
            }

            function l() {
                if (!m()) return null;
                if (!i.show) return null;
                var n = {}, o = {x: i.first.x, y: i.first.y}, a = {x: i.second.x, y: i.second.y};
                return "x" === h(t) && (o.y = 0, a.y = t.height()), "y" === h(t) && (o.x = 0, a.x = t.width()), e.each(t.getAxes(), (function (e, t) {
                    if (t.used) {
                        var i = t.c2p(o[t.direction]), r = t.c2p(a[t.direction]);
                        n[e] = {from: Math.min(i, r), to: Math.max(i, r)}
                    }
                })), n
            }

            function c() {
                var e = l();
                t.getPlaceholder().trigger("plotselected", [e]), e.xaxis && e.yaxis && t.getPlaceholder().trigger("selected", [{
                    x1: e.xaxis.from,
                    y1: e.yaxis.from,
                    x2: e.xaxis.to,
                    y2: e.yaxis.to
                }])
            }

            function u(e, t, i) {
                return t < e ? e : i < t ? i : t
            }

            function h(e) {
                var t = e.getOptions();
                return "smart" === t.selection.mode ? i.currentMode : t.selection.mode
            }

            function p(e, o) {
                var a = t.getPlaceholder().offset(), r = t.getPlotOffset();
                e.x = u(0, o.pageX - a.left - r.left, t.width()), e.y = u(0, o.pageY - a.top - r.top, t.height()), e !== i.first && function (e) {
                    if (i.first) {
                        var t = {x: e.x - i.first.x, y: e.y - i.first.y};
                        Math.abs(t.x) < n ? i.currentMode = "y" : Math.abs(t.y) < n ? i.currentMode = "x" : i.currentMode = "xy"
                    }
                }(e), "y" === h(t) && (e.x = e === i.first ? 0 : t.width()), "x" === h(t) && (e.y = e === i.first ? 0 : t.height())
            }

            function d(e) {
                null != e.pageX && (p(i.second, e), m() ? (i.show = !0, t.triggerRedrawOverlay()) : f(!0))
            }

            function f(e) {
                i.show && (i.show = !1, i.currentMode = "", t.triggerRedrawOverlay(), e || t.getPlaceholder().trigger("plotunselected", []))
            }

            function g(e, i) {
                var n, o, a, r, s = t.getAxes();
                for (var l in s) if ((n = s[l]).direction === i && (e[r = i + n.n + "axis"] || 1 !== n.n || (r = i + "axis"), e[r])) {
                    o = e[r].from, a = e[r].to;
                    break
                }
                if (e[r] || (n = "x" === i ? t.getXAxes()[0] : t.getYAxes()[0], o = e[i + "1"], a = e[i + "2"]), null != o && null != a && a < o) {
                    var c = o;
                    o = a, a = c
                }
                return {from: o, to: a, axis: n}
            }

            function m() {
                var e = t.getOptions().selection.minSize;
                return Math.abs(i.second.x - i.first.x) >= e && Math.abs(i.second.y - i.first.y) >= e
            }

            t.clearSelection = f, t.setSelection = function (e, n) {
                var o;
                "y" === h(t) ? (i.first.x = 0, i.second.x = t.width()) : (o = g(e, "x"), i.first.x = o.axis.p2c(o.from), i.second.x = o.axis.p2c(o.to)), "x" === h(t) ? (i.first.y = 0, i.second.y = t.height()) : (o = g(e, "y"), i.first.y = o.axis.p2c(o.from), i.second.y = o.axis.p2c(o.to)), i.show = !0, t.triggerRedrawOverlay(), !n && m() && c()
            }, t.getSelection = l, t.hooks.bindEvents.push((function (e, t) {
                null != e.getOptions().selection.mode && (e.addEventHandler("dragstart", r, t, 0), e.addEventHandler("drag", a, t, 0), e.addEventHandler("dragend", s, t, 0))
            })), t.hooks.drawOverlay.push((function (t, n) {
                if (i.show && m()) {
                    var o = t.getPlotOffset(), a = t.getOptions();
                    n.save(), n.translate(o.left, o.top);
                    var r = e.color.parse(a.selection.color), s = a.selection.visualization,
                        l = a.selection.displaySelectionDecorations, c = 1;
                    "fill" === s && (c = .8), n.strokeStyle = r.scale("a", c).toString(), n.lineWidth = 1, n.lineJoin = a.selection.shape, n.fillStyle = r.scale("a", .4).toString();
                    var u = Math.min(i.first.x, i.second.x) + .5, p = u, d = Math.min(i.first.y, i.second.y) + .5,
                        f = d, g = Math.abs(i.second.x - i.first.x) - 1, v = Math.abs(i.second.y - i.first.y) - 1;
                    "x" === h(t) && (v += d, d = 0), "y" === h(t) && (g += u, u = 0), "fill" === s ? (n.fillRect(u, d, g, v), n.strokeRect(u, d, g, v)) : (n.fillRect(0, 0, t.width(), t.height()), n.clearRect(u, d, g, v), l && (x = n, b = u, y = d, w = g, k = v, T = p, M = f, S = h(t), P = Math.max(0, Math.min(15, w / 2 - 2, k / 2 - 2)), x.fillStyle = "#ffffff", "xy" === S && (x.beginPath(), x.moveTo(b, y + P), x.lineTo(b - 3, y + P), x.lineTo(b - 3, y - 3), x.lineTo(b + P, y - 3), x.lineTo(b + P, y), x.lineTo(b, y), x.closePath(), x.moveTo(b, y + k - P), x.lineTo(b - 3, y + k - P), x.lineTo(b - 3, y + k + 3), x.lineTo(b + P, y + k + 3), x.lineTo(b + P, y + k), x.lineTo(b, y + k), x.closePath(), x.moveTo(b + w, y + P), x.lineTo(b + w + 3, y + P), x.lineTo(b + w + 3, y - 3), x.lineTo(b + w - P, y - 3), x.lineTo(b + w - P, y), x.lineTo(b + w, y), x.closePath(), x.moveTo(b + w, y + k - P), x.lineTo(b + w + 3, y + k - P), x.lineTo(b + w + 3, y + k + 3), x.lineTo(b + w - P, y + k + 3), x.lineTo(b + w - P, y + k), x.lineTo(b + w, y + k), x.closePath(), x.stroke(), x.fill()), b = T, y = M, "x" === S && (x.beginPath(), x.moveTo(b, y + 15), x.lineTo(b, y - 15), x.lineTo(b - 3, y - 15), x.lineTo(b - 3, y + 15), x.closePath(), x.moveTo(b + w, y + 15), x.lineTo(b + w, y - 15), x.lineTo(b + w + 3, y - 15), x.lineTo(b + w + 3, y + 15), x.closePath(), x.stroke(), x.fill()), "y" === S && (x.beginPath(), x.moveTo(b - 15, y), x.lineTo(b + 15, y), x.lineTo(b + 15, y - 3), x.lineTo(b - 15, y - 3), x.closePath(), x.moveTo(b - 15, y + k), x.lineTo(b + 15, y + k), x.lineTo(b + 15, y + k + 3), x.lineTo(b - 15, y + k + 3), x.closePath(), x.stroke(), x.fill()))), n.restore()
                }
                var x, b, y, w, k, T, M, S, P
            })), t.hooks.shutdown.push((function (e, t) {
                t.unbind("dragstart", r), t.unbind("drag", a), t.unbind("dragend", s)
            }))
        },
        options: {
            selection: {
                mode: null,
                visualization: "focus",
                displaySelectionDecorations: !0,
                color: "#888888",
                shape: "round",
                minSize: 5
            }
        },
        name: "selection",
        version: "1.1"
    })
}(jQuery), function (e) {
    var t = 1, i = e.plot.browser, n = i.getPixelRatio;

    function o(e, o) {
        var u = e.filter(a);
        t = n(o.getContext("2d"));
        var h, p = u.map((function (e) {
            var t, n, o = new Image;
            return new Promise((n = e, (t = o).sourceDescription = '<info className="' + n.className + '" tagName="' + n.tagName + '" id="' + n.id + '">', t.sourceComponent = n, function (e, o) {
                var a, c, u, h, p, d, f, g, m, v, x, b;
                t.onload = function (i) {
                    t.successfullyLoaded = !0, e(t)
                }, t.onabort = function (i) {
                    t.successfullyLoaded = !1, console.log("Can't generate temp image from " + t.sourceDescription + ". It is possible that it is missing some properties or its content is not supported by this browser. Source component:", t.sourceComponent), e(t)
                }, t.onerror = function (i) {
                    t.successfullyLoaded = !1, console.log("Can't generate temp image from " + t.sourceDescription + ". It is possible that it is missing some properties or its content is not supported by this browser. Source component:", t.sourceComponent), e(t)
                }, c = t, "CANVAS" === (a = n).tagName && (u = a, c.src = u.toDataURL("image/png")), "svg" === a.tagName && (h = a, p = c, i.isSafari() || i.isMobileSafari() ? (d = h, f = p, v = l(v = s(r(document), d)), m = function (e) {
                    for (var t = "", i = new Uint8Array(e), n = 0; n < i.length; n += 16384) {
                        t += String.fromCharCode.apply(null, i.subarray(n, n + 16384))
                    }
                    return t
                }(new (TextEncoder || TextEncoderLite)("utf-8").encode(v)), g = "data:image/svg+xml;base64," + btoa(m), f.src = g) : function (e, t) {
                    var i = s(r(document), e);
                    i = l(i);
                    var n = new Blob([i], {type: "image/svg+xml;charset=utf-8"}),
                        o = (self.URL || self.webkitURL || self).createObjectURL(n);
                    t.src = o
                }(h, p)), c.srcImgTagName = a.tagName, x = a, (b = c).genLeft = x.getBoundingClientRect().left, b.genTop = x.getBoundingClientRect().top, "CANVAS" === x.tagName && (b.genRight = b.genLeft + x.width, b.genBottom = b.genTop + x.height), "svg" === x.tagName && (b.genRight = x.getBoundingClientRect().right, b.genBottom = x.getBoundingClientRect().bottom)
            }))
        }));
        return Promise.all(p).then((h = o, function (e) {
            var i = function (e, i) {
                var n = function (e, i) {
                    var n, o = 0;
                    if (0 === e.length) o = -1; else {
                        var a = e[0].genLeft, r = e[0].genTop, s = e[0].genRight, l = e[0].genBottom, c = 0;
                        for (c = 1; c < e.length; c++) a > e[c].genLeft && (a = e[c].genLeft), r > e[c].genTop && (r = e[c].genTop);
                        for (c = 1; c < e.length; c++) s < e[c].genRight && (s = e[c].genRight), l < e[c].genBottom && (l = e[c].genBottom);
                        if (s - a <= 0 || l - r <= 0) o = -2; else {
                            for (i.width = Math.round(s - a), i.height = Math.round(l - r), c = 0; c < e.length; c++) e[c].xCompOffset = e[c].genLeft - a, e[c].yCompOffset = e[c].genTop - r;
                            n = i, void 0 !== e.find((function (e) {
                                return "svg" === e.srcImgTagName
                            })) && t < 1 && (n.width = n.width * t, n.height = n.height * t)
                        }
                    }
                    return o
                }(e, i);
                if (0 === n) for (var o = i.getContext("2d"), a = 0; a < e.length; a++) !0 === e[a].successfullyLoaded && o.drawImage(e[a], e[a].xCompOffset * t, e[a].yCompOffset * t);
                return n
            }(e, h);
            return i
        }), c)
    }

    function a(e) {
        var t = !0, i = !0;
        return null == e ? i = !1 : "CANVAS" === e.tagName && (e.getBoundingClientRect().right !== e.getBoundingClientRect().left && e.getBoundingClientRect().bottom !== e.getBoundingClientRect().top || (t = !1)), i && t && "visible" === window.getComputedStyle(e).visibility
    }

    function r(e) {
        for (var t = e.styleSheets, i = [], n = 0; n < t.length; n++) try {
            for (var o = t[n].cssRules || [], a = 0; a < o.length; a++) {
                var r = o[a];
                i.push(r.cssText)
            }
        } catch (e) {
            console.log("Failed to get some css rules")
        }
        return i
    }

    function s(e, i) {
        return ['<svg class="snapshot ' + i.classList + '" width="' + i.width.baseVal.value * t + '" height="' + i.height.baseVal.value * t + '" viewBox="0 0 ' + i.width.baseVal.value + " " + i.height.baseVal.value + '" xmlns="http://www.w3.org/2000/svg">', "<style>", "/* <![CDATA[ */", e.join("\n"), "/* ]]> */", "</style>", i.innerHTML, "</svg>"].join("\n")
    }

    function l(e) {
        var t = "";
        return e.match(/^<svg[^>]+xmlns="http:\/\/www\.w3\.org\/2000\/svg"/) || (t = e.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"')), e.match(/^<svg[^>]+"http:\/\/www\.w3\.org\/1999\/xlink"/) || (t = e.replace(/^<svg/, '<svg xmlns:xlink="http://www.w3.org/1999/xlink"')), '<?xml version="1.0" standalone="no"?>\r\n' + t
    }

    function c() {
        return -100
    }

    e.plot.composeImages = o, e.plot.plugins.push({
        init: function (e) {
            e.composeImages = o
        }, name: "composeImages", version: "1.0"
    })
}(jQuery), function (e) {
    function t(e) {
        var t = "", i = e.name, n = e.xPos, o = e.yPos, a = e.fillColor, r = e.strokeColor, s = e.strokeWidth;
        switch (i) {
            case"circle":
            default:
                t = '<use xlink:href="#circle" class="legendIcon" x="' + n + '" y="' + o + '" fill="' + a + '" stroke="' + r + '" stroke-width="' + s + '" width="1.5em" height="1.5em"/>';
                break;
            case"diamond":
                t = '<use xlink:href="#diamond" class="legendIcon" x="' + n + '" y="' + o + '" fill="' + a + '" stroke="' + r + '" stroke-width="' + s + '" width="1.5em" height="1.5em"/>';
                break;
            case"cross":
                t = '<use xlink:href="#cross" class="legendIcon" x="' + n + '" y="' + o + '" stroke="' + r + '" stroke-width="' + s + '" width="1.5em" height="1.5em"/>';
                break;
            case"rectangle":
                t = '<use xlink:href="#rectangle" class="legendIcon" x="' + n + '" y="' + o + '" fill="' + a + '" stroke="' + r + '" stroke-width="' + s + '" width="1.5em" height="1.5em"/>';
                break;
            case"plus":
                t = '<use xlink:href="#plus" class="legendIcon" x="' + n + '" y="' + o + '" stroke="' + r + '" stroke-width="' + s + '" width="1.5em" height="1.5em"/>';
                break;
            case"bar":
                t = '<use xlink:href="#bars" class="legendIcon" x="' + n + '" y="' + o + '" fill="' + a + '" width="1.5em" height="1.5em"/>';
                break;
            case"area":
                t = '<use xlink:href="#area" class="legendIcon" x="' + n + '" y="' + o + '" fill="' + a + '" width="1.5em" height="1.5em"/>';
                break;
            case"line":
                t = '<use xlink:href="#line" class="legendIcon" x="' + n + '" y="' + o + '" stroke="' + r + '" stroke-width="' + s + '" width="1.5em" height="1.5em"/>'
        }
        return t
    }

    function i(e, t) {
        for (var i in e) if (e.hasOwnProperty(i) && e[i] !== t[i]) return !0;
        return !1
    }

    e.plot.plugins.push({
        init: function (n) {
            n.hooks.setupGrid.push((function (n) {
                var o = n.getOptions(), a = n.getData(), r = o.legend.labelFormatter, s = o.legend.legendEntries,
                    l = o.legend.plotOffset, c = function (t, i, n) {
                        var o = i, a = t.reduce((function (e, t, i) {
                            var n = o ? o(t.label, t) : t.label;
                            if (!t.hasOwnProperty("label") || n) {
                                var a = {
                                    label: n || "Plot " + (i + 1),
                                    color: t.color,
                                    options: {lines: t.lines, points: t.points, bars: t.bars}
                                };
                                e.push(a)
                            }
                            return e
                        }), []);
                        if (n) if (e.isFunction(n)) a.sort(n); else if ("reverse" === n) a.reverse(); else {
                            var r = "descending" !== n;
                            a.sort((function (e, t) {
                                return e.label === t.label ? 0 : e.label < t.label !== r ? 1 : -1
                            }))
                        }
                        return a
                    }(a, r, o.legend.sorted), u = n.getPlotOffset();
                (function (e, t) {
                    if (!e || !t) return !0;
                    if (e.length !== t.length) return !0;
                    var n, o, a;
                    for (n = 0; n < t.length; n++) {
                        if (o = t[n], a = e[n], o.label !== a.label) return !0;
                        if (o.color !== a.color) return !0;
                        if (i(o.options.lines, a.options.lines)) return !0;
                        if (i(o.options.points, a.options.points)) return !0;
                        if (i(o.options.bars, a.options.bars)) return !0
                    }
                    return !1
                }(s, c) || i(l, u)) && function (i, n, o, a) {
                    if (null != n.legend.container ? e(n.legend.container).html("") : o.find(".legend").remove(), n.legend.show) {
                        var r, s, l, c, u = n.legend.legendEntries = a, h = n.legend.plotOffset = i.getPlotOffset(),
                            p = [], d = 0, f = "", g = n.legend.position, m = n.legend.margin,
                            v = {name: "", label: "", xPos: "", yPos: ""};
                        p[d++] = '<svg class="legendLayer" style="width:inherit;height:inherit;">', p[d++] = '<rect class="background" width="100%" height="100%"/>', p[d++] = '<defs><symbol id="line" fill="none" viewBox="-5 -5 25 25"><polyline points="0,15 5,5 10,10 15,0"/></symbol><symbol id="area" stroke-width="1" viewBox="-5 -5 25 25"><polyline points="0,15 5,5 10,10 15,0, 15,15, 0,15"/></symbol><symbol id="bars" stroke-width="1" viewBox="-5 -5 25 25"><polyline points="1.5,15.5 1.5,12.5, 4.5,12.5 4.5,15.5 6.5,15.5 6.5,3.5, 9.5,3.5 9.5,15.5 11.5,15.5 11.5,7.5 14.5,7.5 14.5,15.5 1.5,15.5"/></symbol><symbol id="circle" viewBox="-5 -5 25 25"><circle cx="0" cy="15" r="2.5"/><circle cx="5" cy="5" r="2.5"/><circle cx="10" cy="10" r="2.5"/><circle cx="15" cy="0" r="2.5"/></symbol><symbol id="rectangle" viewBox="-5 -5 25 25"><rect x="-2.1" y="12.9" width="4.2" height="4.2"/><rect x="2.9" y="2.9" width="4.2" height="4.2"/><rect x="7.9" y="7.9" width="4.2" height="4.2"/><rect x="12.9" y="-2.1" width="4.2" height="4.2"/></symbol><symbol id="diamond" viewBox="-5 -5 25 25"><path d="M-3,15 L0,12 L3,15, L0,18 Z"/><path d="M2,5 L5,2 L8,5, L5,8 Z"/><path d="M7,10 L10,7 L13,10, L10,13 Z"/><path d="M12,0 L15,-3 L18,0, L15,3 Z"/></symbol><symbol id="cross" fill="none" viewBox="-5 -5 25 25"><path d="M-2.1,12.9 L2.1,17.1, M2.1,12.9 L-2.1,17.1 Z"/><path d="M2.9,2.9 L7.1,7.1 M7.1,2.9 L2.9,7.1 Z"/><path d="M7.9,7.9 L12.1,12.1 M12.1,7.9 L7.9,12.1 Z"/><path d="M12.9,-2.1 L17.1,2.1 M17.1,-2.1 L12.9,2.1 Z"/></symbol><symbol id="plus" fill="none" viewBox="-5 -5 25 25"><path d="M0,12 L0,18, M-3,15 L3,15 Z"/><path d="M5,2 L5,8 M2,5 L8,5 Z"/><path d="M10,7 L10,13 M7,10 L13,10 Z"/><path d="M15,-3 L15,3 M12,0 L18,0 Z"/></symbol></defs>';
                        var x = 0, b = [], y = window.getComputedStyle(document.querySelector("body"));
                        for (c = 0; c < u.length; ++c) {
                            var w = c % n.legend.noColumns;
                            r = u[c], v.label = r.label;
                            var k = i.getSurface().getTextInfo("", v.label, {
                                style: y.fontStyle,
                                variant: y.fontVariant,
                                weight: y.fontWeight,
                                size: parseInt(y.fontSize),
                                lineHeight: parseInt(y.lineHeight),
                                family: y.fontFamily
                            }).width;
                            b[w] ? k > b[w] && (b[w] = k + 48) : b[w] = k + 48
                        }
                        for (c = 0; c < u.length; ++c) {
                            var T = c % n.legend.noColumns;
                            r = u[c], l = "", v.label = r.label, v.xPos = x + 3 + "px", x += b[T], (c + 1) % n.legend.noColumns == 0 && (x = 0), v.yPos = 1.5 * Math.floor(c / n.legend.noColumns) + "em", r.options.lines.show && r.options.lines.fill && (v.name = "area", v.fillColor = r.color, l += t(v)), r.options.bars.show && (v.name = "bar", v.fillColor = r.color, l += t(v)), r.options.lines.show && !r.options.lines.fill && (v.name = "line", v.strokeColor = r.color, v.strokeWidth = r.options.lines.lineWidth, l += t(v)), r.options.points.show && (v.name = r.options.points.symbol, v.strokeColor = r.color, v.fillColor = r.options.points.fillColor, v.strokeWidth = r.options.points.lineWidth, l += t(v)), s = '<text x="' + v.xPos + '" y="' + v.yPos + '" text-anchor="start"><tspan dx="2em" dy="1.2em">' + v.label + "</tspan></text>", p[d++] = "<g>" + l + s + "</g>"
                        }
                        p[d++] = "</svg>", null == m[0] && (m = [m, m]), "n" === g.charAt(0) ? f += "top:" + (m[1] + h.top) + "px;" : "s" === g.charAt(0) && (f += "bottom:" + (m[1] + h.bottom) + "px;"), "e" === g.charAt(1) ? f += "right:" + (m[0] + h.right) + "px;" : "w" === g.charAt(1) && (f += "left:" + (m[0] + h.left) + "px;");
                        var M = 6;
                        for (c = 0; c < b.length; ++c) M += b[c];
                        var S, P = 1.6 * Math.ceil(u.length / n.legend.noColumns);
                        n.legend.container ? (S = e(p.join("")).appendTo(n.legend.container)[0], n.legend.container.style.width = M + "px", n.legend.container.style.height = P + "em") : ((S = e('<div class="legend" style="position:absolute;' + f + '">' + p.join("") + "</div>").appendTo(o)).css("width", M + "px"), S.css("height", P + "em"), S.css("pointerEvents", "none"))
                    }
                }(n, o, n.getPlaceholder(), c)
            }))
        },
        options: {
            legend: {
                show: !1,
                noColumns: 1,
                labelFormatter: null,
                container: null,
                position: "ne",
                margin: 5,
                sorted: null
            }
        },
        name: "legend",
        version: "1.0"
    })
}(jQuery), function (e, t, i) {
    var n, o = [], a = e.resize = e.extend(e.resize, {}), r = !1, s = "setTimeout", l = "resize",
        c = l + "-special-event", u = "pendingDelay", h = "activeDelay", p = "throttleWindow";

    function d(i) {
        !0 === r && (r = i || 1);
        for (var s = o.length - 1; s >= 0; s--) {
            var h = e(o[s]);
            if (h[0] == t || h.is(":visible")) {
                var p = h.width(), f = h.height(), g = h.data(c);
                !g || p === g.w && f === g.h || (h.trigger(l, [g.w = p, g.h = f]), r = i || !0)
            } else (g = h.data(c)).w = 0, g.h = 0
        }
        null !== n && (r && (null == i || i - r < 1e3) ? n = t.requestAnimationFrame(d) : (n = setTimeout(d, a[u]), r = !1))
    }

    a[u] = 200, a[h] = 20, a[p] = !0, e.event.special[l] = {
        setup: function () {
            if (!a[p] && this[s]) return !1;
            var t = e(this);
            o.push(this), t.data(c, {w: t.width(), h: t.height()}), 1 === o.length && (n = i, d())
        }, teardown: function () {
            if (!a[p] && this[s]) return !1;
            for (var t = e(this), i = o.length - 1; i >= 0; i--) if (o[i] == this) {
                o.splice(i, 1);
                break
            }
            t.removeData(c), o.length || (r ? cancelAnimationFrame(n) : clearTimeout(n), n = null)
        }, add: function (t) {
            if (!a[p] && this[s]) return !1;
            var n;

            function o(t, o, a) {
                var r = e(this), s = r.data(c) || {};
                s.w = o !== i ? o : r.width(), s.h = a !== i ? a : r.height(), n.apply(this, arguments)
            }

            if (e.isFunction(t)) return n = t, o;
            n = t.handler, t.handler = o
        }
    }, t.requestAnimationFrame || (t.requestAnimationFrame = t.webkitRequestAnimationFrame || t.mozRequestAnimationFrame || t.oRequestAnimationFrame || t.msRequestAnimationFrame || function (e, i) {
        return t.setTimeout((function () {
            e((new Date).getTime())
        }), a[h])
    }), t.cancelAnimationFrame || (t.cancelAnimationFrame = t.webkitCancelRequestAnimationFrame || t.mozCancelRequestAnimationFrame || t.oCancelRequestAnimationFrame || t.msCancelRequestAnimationFrame || clearTimeout)
}(jQuery, window), jQuery.plot.plugins.push({
    init: function (e) {
        function t() {
            var t = e.getPlaceholder();
            0 !== t.width() && 0 !== t.height() && (e.resize(), e.setupGrid(), e.draw())
        }

        e.hooks.bindEvents.push((function (e, i) {
            e.getPlaceholder().resize(t)
        })), e.hooks.shutdown.push((function (e, i) {
            e.getPlaceholder().unbind("resize", t)
        }))
    }, options: {}, name: "resize", version: "1.0"
}), function (e) {
    function t(e, t, i, n) {
        var o = "categories" === t.xaxis.options.mode, a = "categories" === t.yaxis.options.mode;
        if (o || a) {
            var r = n.format;
            if (!r) {
                var s = t;
                if ((r = []).push({x: !0, number: !0, required: !0, computeRange: !0}), r.push({
                    y: !0,
                    number: !0,
                    required: !0,
                    computeRange: !0
                }), s.bars.show || s.lines.show && s.lines.fill) {
                    var l = !!(s.bars.show && s.bars.zero || s.lines.show && s.lines.zero);
                    r.push({
                        y: !0,
                        number: !0,
                        required: !1,
                        defaultValue: 0,
                        computeRange: l
                    }), s.bars.horizontal && (delete r[r.length - 1].y, r[r.length - 1].x = !0)
                }
                n.format = r
            }
            for (var c = 0; c < r.length; ++c) r[c].x && o && (r[c].number = !1), r[c].y && a && (r[c].number = !1, r[c].computeRange = !1)
        }
    }

    function i(e) {
        var t = [];
        for (var i in e.categories) {
            var n = e.categories[i];
            n >= e.min && n <= e.max && t.push([n, i])
        }
        return t.sort((function (e, t) {
            return e[0] - t[0]
        })), t
    }

    function n(t, n, o) {
        if ("categories" === t[n].options.mode) {
            if (!t[n].categories) {
                var a = {}, r = t[n].options.categories || {};
                if (e.isArray(r)) for (var s = 0; s < r.length; ++s) a[r[s]] = s; else for (var l in r) a[l] = r[l];
                t[n].categories = a
            }
            t[n].options.ticks || (t[n].options.ticks = i), function (e, t, i) {
                for (var n = e.points, o = e.pointsize, a = e.format, r = t.charAt(0), s = function (e) {
                    var t = -1;
                    for (var i in e) e[i] > t && (t = e[i]);
                    return t + 1
                }(i), l = 0; l < n.length; l += o) if (null != n[l]) for (var c = 0; c < o; ++c) {
                    var u = n[l + c];
                    null != u && a[c][r] && (u in i || (i[u] = s, ++s), n[l + c] = i[u])
                }
            }(o, n, t[n].categories)
        }
    }

    function o(e, t, i) {
        n(t, "xaxis", i), n(t, "yaxis", i)
    }

    e.plot.plugins.push({
        init: function (e) {
            e.hooks.processRawData.push(t), e.hooks.processDatapoints.push(o)
        }, options: {xaxis: {categories: null}, yaxis: {categories: null}}, name: "categories", version: "1.0"
    })
}(jQuery), function (e) {
    var t = {
        series: {
            pie: {
                show: !1,
                radius: "auto",
                innerRadius: 0,
                startAngle: 1.5,
                tilt: 1,
                shadow: {left: 5, top: 15, alpha: .02},
                offset: {top: 0, left: "auto"},
                stroke: {color: "#fff", width: 1},
                label: {
                    show: "auto", formatter: function (e, t) {
                        return "<div style='font-size:x-small;text-align:center;padding:2px;color:" + t.color + ";'>" + e + "<br/>" + Math.round(t.percent) + "%</div>"
                    }, radius: 1, background: {color: null, opacity: 0}, threshold: 0
                },
                combine: {threshold: -1, color: null, label: "Other"},
                highlight: {opacity: .5}
            }
        }
    };
    e.plot.plugins.push({
        init: function (t) {
            var i = null, n = null, o = null, a = null, r = null, s = null, l = !1, c = null, u = [];

            function h(t, a, r) {
                l || (l = !0, i = t.getCanvas(), n = e(i).parent(), o = t.getOptions(), t.setData(function (t) {
                    var i, n, a = 0, r = 0, s = 0, l = o.series.pie.combine.color, c = [];
                    for (i = 0; i < t.length; ++i) n = t[i].data, e.isArray(n) && 1 === n.length && (n = n[0]), e.isArray(n) ? !isNaN(parseFloat(n[1])) && isFinite(n[1]) ? n[1] = +n[1] : n[1] = 0 : n = !isNaN(parseFloat(n)) && isFinite(n) ? [1, +n] : [1, 0], t[i].data = [n];
                    for (i = 0; i < t.length; ++i) a += t[i].data[0][1];
                    for (i = 0; i < t.length; ++i) (n = t[i].data[0][1]) / a <= o.series.pie.combine.threshold && (r += n, s++, l || (l = t[i].color));
                    for (i = 0; i < t.length; ++i) n = t[i].data[0][1], (s < 2 || n / a > o.series.pie.combine.threshold) && c.push(e.extend(t[i], {
                        data: [[1, n]],
                        color: t[i].color,
                        label: t[i].label,
                        angle: n * Math.PI * 2 / a,
                        percent: n / (a / 100)
                    }));
                    s > 1 && c.push({
                        data: [[1, r]],
                        color: l,
                        label: o.series.pie.combine.label,
                        angle: r * Math.PI * 2 / a,
                        percent: r / (a / 100)
                    });
                    return c
                }(t.getData())))
            }

            function p(t, i) {
                if (n) {
                    var u = t.getPlaceholder().width(), h = t.getPlaceholder().height(),
                        p = n.children().filter(".legend").children().width() || 0;
                    c = i, l = !1, a = Math.min(u, h / o.series.pie.tilt) / 2, s = h / 2 + o.series.pie.offset.top, r = u / 2, "auto" === o.series.pie.offset.left ? (o.legend.position.match("w") ? r += p / 2 : r -= p / 2, r < a ? r = a : r > u - a && (r = u - a)) : r += o.series.pie.offset.left;
                    var f = t.getData(), g = 0;
                    do {
                        g > 0 && (a *= .95), g += 1, m(), o.series.pie.tilt <= .8 && v()
                    } while (!x() && g < 10);
                    g >= 10 && (m(), n.prepend("<div class='error'>Could not draw pie with labels contained inside canvas</div>")), t.setSeries && t.insertLegend && (t.setSeries(f), t.insertLegend())
                }

                function m() {
                    c.clearRect(0, 0, u, h), n.children().filter(".pieLabel, .pieLabelBackground").remove()
                }

                function v() {
                    var e = o.series.pie.shadow.left, t = o.series.pie.shadow.top, i = o.series.pie.shadow.alpha,
                        n = o.series.pie.radius > 1 ? o.series.pie.radius : a * o.series.pie.radius;
                    if (!(n >= u / 2 - e || n * o.series.pie.tilt >= h / 2 - t || n <= 10)) {
                        c.save(), c.translate(e, t), c.globalAlpha = i, c.fillStyle = "#000", c.translate(r, s), c.scale(1, o.series.pie.tilt);
                        for (var l = 1; l <= 10; l++) c.beginPath(), c.arc(0, 0, n, 0, 2 * Math.PI, !1), c.fill(), n -= l;
                        c.restore()
                    }
                }

                function x() {
                    var t, i = Math.PI * o.series.pie.startAngle,
                        l = o.series.pie.radius > 1 ? o.series.pie.radius : a * o.series.pie.radius;
                    c.save(), c.translate(r, s), c.scale(1, o.series.pie.tilt), c.save();
                    var p = i;
                    for (t = 0; t < f.length; ++t) f[t].startAngle = p, g(f[t].angle, f[t].color, !0);
                    if (c.restore(), o.series.pie.stroke.width > 0) {
                        for (c.save(), c.lineWidth = o.series.pie.stroke.width, p = i, t = 0; t < f.length; ++t) g(f[t].angle, o.series.pie.stroke.color, !1);
                        c.restore()
                    }
                    return d(c), c.restore(), !o.series.pie.label.show || function () {
                        for (var t = i, l = o.series.pie.label.radius > 1 ? o.series.pie.label.radius : a * o.series.pie.label.radius, c = 0; c < f.length; ++c) {
                            if (f[c].percent >= 100 * o.series.pie.label.threshold && !p(f[c], t, c)) return !1;
                            t += f[c].angle
                        }
                        return !0;

                        function p(t, i, a) {
                            if (0 === t.data[0][1]) return !0;
                            var c, p = o.legend.labelFormatter, d = o.series.pie.label.formatter;
                            c = p ? p(t.label, t) : t.label, d && (c = d(c, t));
                            var f = (i + t.angle + i) / 2, g = r + Math.round(Math.cos(f) * l),
                                m = s + Math.round(Math.sin(f) * l) * o.series.pie.tilt,
                                v = "<span class='pieLabel' id='pieLabel" + a + "' style='position:absolute;top:" + m + "px;left:" + g + "px;'>" + c + "</span>";
                            n.append(v);
                            var x = n.children("#pieLabel" + a), b = m - x.height() / 2, y = g - x.width() / 2;
                            if (x.css("top", b), x.css("left", y), 0 - b > 0 || 0 - y > 0 || h - (b + x.height()) < 0 || u - (y + x.width()) < 0) return !1;
                            if (0 !== o.series.pie.label.background.opacity) {
                                var w = o.series.pie.label.background.color;
                                null == w && (w = t.color);
                                var k = "top:" + b + "px;left:" + y + "px;";
                                e("<div class='pieLabelBackground' style='position:absolute;width:" + x.width() + "px;height:" + x.height() + "px;" + k + "background-color:" + w + ";'></div>").css("opacity", o.series.pie.label.background.opacity).insertBefore(x)
                            }
                            return !0
                        }
                    }();

                    function g(e, t, i) {
                        e <= 0 || isNaN(e) || (i ? c.fillStyle = t : (c.strokeStyle = t, c.lineJoin = "round"), c.beginPath(), Math.abs(e - 2 * Math.PI) > 1e-9 && c.moveTo(0, 0), c.arc(0, 0, l, p, p + e / 2, !1), c.arc(0, 0, l, p + e / 2, p + e, !1), c.closePath(), p += e, i ? c.fill() : c.stroke())
                    }
                }
            }

            function d(e) {
                if (o.series.pie.innerRadius > 0) {
                    e.save();
                    var t = o.series.pie.innerRadius > 1 ? o.series.pie.innerRadius : a * o.series.pie.innerRadius;
                    e.globalCompositeOperation = "destination-out", e.beginPath(), e.fillStyle = o.series.pie.stroke.color, e.arc(0, 0, t, 0, 2 * Math.PI, !1), e.fill(), e.closePath(), e.restore(), e.save(), e.beginPath(), e.strokeStyle = o.series.pie.stroke.color, e.arc(0, 0, t, 0, 2 * Math.PI, !1), e.stroke(), e.closePath(), e.restore()
                }
            }

            function f(e, t) {
                for (var i = !1, n = -1, o = e.length, a = o - 1; ++n < o; a = n) (e[n][1] <= t[1] && t[1] < e[a][1] || e[a][1] <= t[1] && t[1] < e[n][1]) && t[0] < (e[a][0] - e[n][0]) * (t[1] - e[n][1]) / (e[a][1] - e[n][1]) + e[n][0] && (i = !i);
                return i
            }

            function g(e) {
                v("plothover", e)
            }

            function m(e) {
                v("plotclick", e)
            }

            function v(e, i) {
                var l = t.offset(), h = function (e, i) {
                    for (var n, o, l = t.getData(), u = t.getOptions(), h = u.series.pie.radius > 1 ? u.series.pie.radius : a * u.series.pie.radius, p = 0; p < l.length; ++p) {
                        var d = l[p];
                        if (d.pie.show) {
                            if (c.save(), c.beginPath(), c.moveTo(0, 0), c.arc(0, 0, h, d.startAngle, d.startAngle + d.angle / 2, !1), c.arc(0, 0, h, d.startAngle + d.angle / 2, d.startAngle + d.angle, !1), c.closePath(), n = e - r, o = i - s, c.isPointInPath) {
                                if (c.isPointInPath(e - r, i - s)) return c.restore(), {
                                    datapoint: [d.percent, d.data],
                                    dataIndex: 0,
                                    series: d,
                                    seriesIndex: p
                                }
                            } else if (f([[0, 0], [h * Math.cos(d.startAngle), h * Math.sin(d.startAngle)], [h * Math.cos(d.startAngle + d.angle / 4), h * Math.sin(d.startAngle + d.angle / 4)], [h * Math.cos(d.startAngle + d.angle / 2), h * Math.sin(d.startAngle + d.angle / 2)], [h * Math.cos(d.startAngle + d.angle / 1.5), h * Math.sin(d.startAngle + d.angle / 1.5)], [h * Math.cos(d.startAngle + d.angle), h * Math.sin(d.startAngle + d.angle)]], [n, o])) return c.restore(), {
                                datapoint: [d.percent, d.data],
                                dataIndex: 0,
                                series: d,
                                seriesIndex: p
                            };
                            c.restore()
                        }
                    }
                    return null
                }(parseInt(i.pageX - l.left), parseInt(i.pageY - l.top));
                if (o.grid.autoHighlight) for (var p = 0; p < u.length; ++p) {
                    var d = u[p];
                    d.auto !== e || h && d.series === h.series || x(d.series)
                }
                h && function (e, i) {
                    var n = b(e);
                    -1 === n ? (u.push({series: e, auto: i}), t.triggerRedrawOverlay()) : i || (u[n].auto = !1)
                }(h.series, e);
                var g = {pageX: i.pageX, pageY: i.pageY};
                n.trigger(e, [g, h])
            }

            function x(e) {
                null == e && (u = [], t.triggerRedrawOverlay());
                var i = b(e);
                -1 !== i && (u.splice(i, 1), t.triggerRedrawOverlay())
            }

            function b(e) {
                for (var t = 0; t < u.length; ++t) {
                    if (u[t].series === e) return t
                }
                return -1
            }

            t.hooks.processOptions.push((function (e, t) {
                t.series.pie.show && (t.grid.show = !1, "auto" === t.series.pie.label.show && (t.legend.show ? t.series.pie.label.show = !1 : t.series.pie.label.show = !0), "auto" === t.series.pie.radius && (t.series.pie.label.show ? t.series.pie.radius = 3 / 4 : t.series.pie.radius = 1), t.series.pie.tilt > 1 ? t.series.pie.tilt = 1 : t.series.pie.tilt < 0 && (t.series.pie.tilt = 0))
            })), t.hooks.bindEvents.push((function (e, t) {
                var i = e.getOptions();
                i.series.pie.show && (i.grid.hoverable && (t.unbind("mousemove").mousemove(g), t.bind("mouseleave", g)), i.grid.clickable && t.unbind("click").click(m))
            })), t.hooks.shutdown.push((function (e, t) {
                t.unbind("mousemove", g), t.unbind("mouseleave", g), t.unbind("click", m), u = []
            })), t.hooks.processDatapoints.push((function (e, t, i, n) {
                e.getOptions().series.pie.show && h(e, t, i)
            })), t.hooks.drawOverlay.push((function (e, t) {
                e.getOptions().series.pie.show && function (e, t) {
                    var i = e.getOptions(), n = i.series.pie.radius > 1 ? i.series.pie.radius : a * i.series.pie.radius;
                    t.save(), t.translate(r, s), t.scale(1, i.series.pie.tilt);
                    for (var o = 0; o < u.length; ++o) l(u[o].series);

                    function l(e) {
                        e.angle <= 0 || isNaN(e.angle) || (t.fillStyle = "rgba(255, 255, 255, " + i.series.pie.highlight.opacity + ")", t.beginPath(), Math.abs(e.angle - 2 * Math.PI) > 1e-9 && t.moveTo(0, 0), t.arc(0, 0, n, e.startAngle, e.startAngle + e.angle / 2, !1), t.arc(0, 0, n, e.startAngle + e.angle / 2, e.startAngle + e.angle, !1), t.closePath(), t.fill())
                    }

                    d(t), t.restore()
                }(e, t)
            })), t.hooks.draw.push((function (e, t) {
                e.getOptions().series.pie.show && p(e, t)
            }))
        }, options: t, name: "pie", version: "1.1"
    })
}(jQuery), jQuery.plot.plugins.push({
    init: function (e) {
        e.hooks.processDatapoints.push((function (e, t, i) {
            if (null != t.stack && !1 !== t.stack) {
                var n = t.bars.show || t.lines.show && t.lines.fill,
                    o = i.pointsize > 2 && (t.bars.horizontal ? i.format[2].x : i.format[2].y);
                n && !o && function (e, t) {
                    for (var i = [], n = 0; n < t.points.length; n += 2) i.push(t.points[n]), i.push(t.points[n + 1]), i.push(0);
                    t.format.push({
                        x: e.bars.horizontal,
                        y: !e.bars.horizontal,
                        number: !0,
                        required: !1,
                        computeRange: "none" !== e.yaxis.options.autoScale,
                        defaultValue: 0
                    }), t.points = i, t.pointsize = 3
                }(t, i);
                var a = function (e, t) {
                    for (var i = null, n = 0; n < t.length && e !== t[n]; ++n) t[n].stack === e.stack && (i = t[n]);
                    return i
                }(t, e.getData());
                if (a) {
                    for (var r, s, l, c, u, h, p, d, f = i.pointsize, g = i.points, m = a.datapoints.pointsize, v = a.datapoints.points, x = [], b = t.lines.show, y = t.bars.horizontal, w = b && t.lines.steps, k = !0, T = y ? 1 : 0, M = y ? 0 : 1, S = 0, P = 0; !(S >= g.length);) {
                        if (p = x.length, null == g[S]) {
                            for (d = 0; d < f; ++d) x.push(g[S + d]);
                            S += f
                        } else if (P >= v.length) {
                            if (!b) for (d = 0; d < f; ++d) x.push(g[S + d]);
                            S += f
                        } else if (null == v[P]) {
                            for (d = 0; d < f; ++d) x.push(null);
                            k = !0, P += m
                        } else {
                            if (r = g[S + T], s = g[S + M], c = v[P + T], u = v[P + M], h = 0, r === c) {
                                for (d = 0; d < f; ++d) x.push(g[S + d]);
                                x[p + M] += u, h = u, S += f, P += m
                            } else if (r > c) {
                                if (b && S > 0 && null != g[S - f]) {
                                    for (l = s + (g[S - f + M] - s) * (c - r) / (g[S - f + T] - r), x.push(c), x.push(l + u), d = 2; d < f; ++d) x.push(g[S + d]);
                                    h = u
                                }
                                P += m
                            } else {
                                if (k && b) {
                                    S += f;
                                    continue
                                }
                                for (d = 0; d < f; ++d) x.push(g[S + d]);
                                b && P > 0 && null != v[P - m] && (h = u + (v[P - m + M] - u) * (r - c) / (v[P - m + T] - c)), x[p + M] += h, S += f
                            }
                            k = !1, p !== x.length && n && (x[p + 2] += h)
                        }
                        if (w && p !== x.length && p > 0 && null !== x[p] && x[p] !== x[p - f] && x[p + 1] !== x[p - f + 1]) {
                            for (d = 0; d < f; ++d) x[p + f + d] = x[p + d];
                            x[p + 1] = x[p - f + 1]
                        }
                    }
                    i.points = x
                }
            }
        }))
    }, options: {series: {stack: null}}, name: "stack", version: "1.2"
}), jQuery.plot.plugins.push({
    init: function (e) {
        var t = {x: -1, y: -1, locked: !1, highlighted: !1};

        function i(i) {
            t.locked || -1 !== t.x && (t.x = -1, e.triggerRedrawOverlay())
        }

        function n(i) {
            var n = e.offset();
            if (t.locked) {
                var o = Math.max(0, Math.min(i.pageX - n.left, e.width())),
                    a = Math.max(0, Math.min(i.pageY - n.top, e.height()));
                o > t.x - 4 && o < t.x + 4 && a > t.y - 4 && a < t.y + 4 ? t.highlighted || (t.highlighted = !0, e.triggerRedrawOverlay()) : t.highlighted && (t.highlighted = !1, e.triggerRedrawOverlay())
            } else e.getSelection && e.getSelection() ? t.x = -1 : (t.x = Math.max(0, Math.min(i.pageX - n.left, e.width())), t.y = Math.max(0, Math.min(i.pageY - n.top, e.height())), e.triggerRedrawOverlay())
        }

        e.setCrosshair = function (i) {
            if (i) {
                var n = e.p2c(i);
                t.x = Math.max(0, Math.min(n.left, e.width())), t.y = Math.max(0, Math.min(n.top, e.height()))
            } else t.x = -1;
            e.triggerRedrawOverlay()
        }, e.clearCrosshair = e.setCrosshair, e.lockCrosshair = function (i) {
            i && e.setCrosshair(i), t.locked = !0
        }, e.unlockCrosshair = function () {
            t.locked = !1, t.rect = null
        }, e.hooks.bindEvents.push((function (e, t) {
            e.getOptions().crosshair.mode && (t.mouseout(i), t.mousemove(n))
        })), e.hooks.drawOverlay.push((function (e, i) {
            var n = e.getOptions().crosshair;
            if (n.mode) {
                var o = e.getPlotOffset();
                if (i.save(), i.translate(o.left, o.top), -1 !== t.x) {
                    var a = e.getOptions().crosshair.lineWidth % 2 ? .5 : 0;
                    if (i.strokeStyle = n.color, i.lineWidth = n.lineWidth, i.lineJoin = "round", i.beginPath(), -1 !== n.mode.indexOf("x")) {
                        var r = Math.floor(t.x) + a;
                        i.moveTo(r, 0), i.lineTo(r, e.height())
                    }
                    if (-1 !== n.mode.indexOf("y")) {
                        var s = Math.floor(t.y) + a;
                        i.moveTo(0, s), i.lineTo(e.width(), s)
                    }
                    t.locked && (t.highlighted ? i.fillStyle = "orange" : i.fillStyle = n.color, i.fillRect(Math.floor(t.x) + a - 4, Math.floor(t.y) + a - 4, 8, 8)), i.stroke()
                }
                i.restore()
            }
        })), e.hooks.shutdown.push((function (e, t) {
            t.unbind("mouseout", i), t.unbind("mousemove", n)
        }))
    },
    options: {crosshair: {mode: null, color: "rgba(170, 0, 0, 0.80)", lineWidth: 1}},
    name: "crosshair",
    version: "1.0"
}), function (e) {
    function t(e, t, i, n, o, a) {
        this.axisName = e, this.position = t, this.padding = i, this.placeholder = n, this.axisLabel = o, this.surface = a, this.width = 0, this.height = 0, this.elem = null
    }

    t.prototype.calculateSize = function () {
        var e = this.axisName + "Label", t = e + "Layer", i = e + " axisLabels",
            n = this.surface.getTextInfo(t, this.axisLabel, i);
        this.labelWidth = n.width, this.labelHeight = n.height, "left" === this.position || "right" === this.position ? (this.width = this.labelHeight + this.padding, this.height = 0) : (this.width = 0, this.height = this.labelHeight + this.padding)
    }, t.prototype.transforms = function (e, t, i, n) {
        var o, a, r = [];
        if (0 === t && 0 === i || ((o = n.createSVGTransform()).setTranslate(t, i), r.push(o)), 0 !== e) {
            a = n.createSVGTransform();
            var s = Math.round(this.labelWidth / 2);
            a.setRotate(e, s, 0), r.push(a)
        }
        return r
    }, t.prototype.calculateOffsets = function (e) {
        var t = {x: 0, y: 0, degrees: 0};
        return "bottom" === this.position ? (t.x = e.left + e.width / 2 - this.labelWidth / 2, t.y = e.top + e.height - this.labelHeight) : "top" === this.position ? (t.x = e.left + e.width / 2 - this.labelWidth / 2, t.y = e.top) : "left" === this.position ? (t.degrees = -90, t.x = e.left - this.labelWidth / 2, t.y = e.height / 2 + e.top) : "right" === this.position && (t.degrees = 90, t.x = e.left + e.width - this.labelWidth / 2, t.y = e.height / 2 + e.top), t.x = Math.round(t.x), t.y = Math.round(t.y), t
    }, t.prototype.cleanup = function () {
        var e = this.axisName + "Label", t = e + "Layer", i = e + " axisLabels";
        this.surface.removeText(t, 0, 0, this.axisLabel, i)
    }, t.prototype.draw = function (e) {
        var t = this.axisName + "Label", i = t + "Layer", n = t + " axisLabels", o = this.calculateOffsets(e),
            a = {position: "absolute", bottom: "", right: "", display: "inline-block", "white-space": "nowrap"},
            r = this.surface.getSVGLayer(i), s = this.transforms(o.degrees, o.x, o.y, r.parentNode);
        this.surface.addText(i, 0, 0, this.axisLabel, n, void 0, void 0, void 0, void 0, s), this.surface.render(), Object.keys(a).forEach((function (e) {
            r.style[e] = a[e]
        }))
    }, e.plot.plugins.push({
        init: function (i) {
            i.hooks.processOptions.push((function (i, n) {
                if (n.axisLabels.show) {
                    var o = {};
                    i.hooks.axisReserveSpace.push((function (e, i) {
                        var n = i.options, a = i.direction + i.n;
                        if (i.labelHeight += i.boxPosition.centerY, i.labelWidth += i.boxPosition.centerX, n && n.axisLabel && i.show) {
                            var r = void 0 === n.axisLabelPadding ? 2 : n.axisLabelPadding, s = o[a];
                            s || (s = new t(a, n.position, r, e.getPlaceholder()[0], n.axisLabel, e.getSurface()), o[a] = s), s.calculateSize(), i.labelHeight += s.height, i.labelWidth += s.width
                        }
                    })), i.hooks.draw.push((function (t, i) {
                        e.each(t.getAxes(), (function (e, t) {
                            var i = t.options;
                            if (i && i.axisLabel && t.show) {
                                var n = t.direction + t.n;
                                o[n].draw(t.box)
                            }
                        }))
                    })), i.hooks.shutdown.push((function (e, t) {
                        for (var i in o) o[i].cleanup()
                    }))
                }
            }))
        }, options: {axisLabels: {show: !0}}, name: "axisLabels", version: "3.0"
    })
}(jQuery);