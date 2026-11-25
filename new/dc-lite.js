/* Minimal runtime for the Natural Angle screens: {{path}} holes, <sc-if>, <sc-for>, onClick bindings. */
(function () {
  function get(scope, path) {
    path = path.trim();
    if (path === 'true') return true;
    if (path === 'false') return false;
    return path.split('.').reduce(function (o, k) { return o == null ? undefined : o[k]; }, scope);
  }
  var WHOLE = /^\s*\{\{([^}]+)\}\}\s*$/;
  function interp(str, scope) {
    return str.replace(/\{\{([^}]+)\}\}/g, function (_, p) { var v = get(scope, p); return v == null ? '' : String(v); });
  }
  function walk(node, scope) {
    if (node.nodeType === 3) {
      if (node.nodeValue.indexOf('{{') > -1) node.nodeValue = interp(node.nodeValue, scope);
      return;
    }
    if (node.nodeType !== 1) return;
    var tag = node.tagName.toLowerCase();
    if (tag === 'sc-for') {
      var m = (node.getAttribute('list') || '').match(WHOLE);
      var list = m ? get(scope, m[1]) : [];
      var as = node.getAttribute('as') || 'item';
      var frag = document.createDocumentFragment();
      (list || []).forEach(function (item, i) {
        var s = Object.create(scope); s[as] = item; s.$index = i;
        Array.prototype.forEach.call(node.childNodes, function (c) {
          var cl = c.cloneNode(true); var holder = document.createElement('div'); holder.appendChild(cl);
          walk(cl, s); while (holder.firstChild) frag.appendChild(holder.firstChild);
        });
      });
      node.parentNode.replaceChild(frag, node);
      return;
    }
    if (tag === 'sc-if') {
      var mv = (node.getAttribute('value') || '').match(WHOLE);
      var ok = mv ? !!get(scope, mv[1]) : false;
      if (!ok) { node.parentNode.removeChild(node); return; }
      var kids = Array.prototype.slice.call(node.childNodes);
      kids.forEach(function (c) { node.parentNode.insertBefore(c, node); });
      node.parentNode.removeChild(node);
      kids.forEach(function (c) { if (c.parentNode) walk(c, scope); });
      return;
    }
    Array.prototype.slice.call(node.attributes).forEach(function (a) {
      var n = a.name, v = a.value;
      if (n.indexOf('hint-') === 0) { node.removeAttribute(n); return; }
      if (v.indexOf('{{') < 0) return;
      if (n.indexOf('on') === 0) {
        var mm = v.match(WHOLE); var fn = mm ? get(scope, mm[1]) : null;
        node.removeAttribute(n);
        if (typeof fn === 'function') node.addEventListener(n.slice(2).toLowerCase(), function (e) { fn(e); });
        return;
      }
      node.setAttribute(n, interp(v, scope));
    });
    Array.prototype.slice.call(node.childNodes).forEach(function (c) { walk(c, scope); });
  }
  window.DCLogic = function DCLogic(props) { this.props = props || {}; this.state = {}; };
  window.DCLogic.prototype.setState = function (p) {
    var patch = typeof p === 'function' ? p(this.state) : p;
    this.state = Object.assign({}, this.state, patch);
    if (this.__persist) { try { localStorage.setItem(this.__persist, JSON.stringify(this.state)); } catch (e) {} }
    if (this.__render) this.__render();
  };
  window.DC = {
    mount: function (Comp, props, persistKey) {
      var tpl = document.getElementById('tpl');
      var app = document.getElementById('app');
      var c = new Comp(props || {});
      if (!c.state) c.state = {};
      if (persistKey) {
        c.__persist = persistKey;
        try { var saved = JSON.parse(localStorage.getItem(persistKey) || 'null'); if (saved) c.state = Object.assign({}, c.state, saved); } catch (e) {}
      }
      c.__render = function () {
        var vals = c.renderVals ? c.renderVals() : {};
        var frag = tpl.content.cloneNode(true);
        var holder = document.createElement('div'); holder.appendChild(frag);
        Array.prototype.slice.call(holder.childNodes).forEach(function (n) { walk(n, vals); });
        app.innerHTML = '';
        while (holder.firstChild) app.appendChild(holder.firstChild);
        document.dispatchEvent(new CustomEvent('dc:render'));
      };
      c.__render();
      return c;
    }
  };
})();
