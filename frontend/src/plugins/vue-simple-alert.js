import Vue from 'vue'
import Swal from 'sweetalert2'

let __assign = (this && this.__assign) || function () {
  __assign = Object.assign || function (t) {
    for (let s, i = 1, n = arguments.length; i < n; i++) {
      s = arguments[i]
      for (let p in s) {
        if (Object.prototype.hasOwnProperty.call(s, p)) {
          t[p] = s[p]
        }
      }
    }
    return t
  }
  return __assign.apply(this, arguments)
}

let VueSimpleAlert = (function () {
  function VueSimpleAlert () {
  }
  VueSimpleAlert.alert = function (message, title, type, options) {
    return new Promise(function (resolve) {
      let mixedOptions = __assign(__assign({}, VueSimpleAlert.globalOptions), options)
      mixedOptions.title = title || mixedOptions.title
      mixedOptions.text = message || mixedOptions.text
      mixedOptions.type = type || mixedOptions.type
      Swal.fire(mixedOptions)
        .then(function () {
          resolve(true)
        })
        .catch(function () {
          resolve(true)
        })
    })
  }
  VueSimpleAlert.confirm = function (message, title, type, options) {
    return new Promise(function (resolve, reject) {
      let mixedOptions = __assign(__assign({}, VueSimpleAlert.globalOptions), options)
      mixedOptions.title = title || mixedOptions.title
      mixedOptions.text = message || mixedOptions.text
      mixedOptions.type = type || mixedOptions.type
      mixedOptions.showCancelButton = true
      Swal.fire(mixedOptions)
        .then(function (r) {
          if (r.value === true) {
            resolve(true)
          } else {
            reject(new Error('Could not fire sweetalert2'))
          }
        })
        .catch(function () { return reject(new Error('Could not fire sweetalert2')) })
    })
  }
  VueSimpleAlert.prompt = function (message, defaultText, title, type, options) {
    return new Promise(function (resolve, reject) {
      let mixedOptions = __assign(__assign({}, VueSimpleAlert.globalOptions), options)
      mixedOptions.title = title || mixedOptions.title
      mixedOptions.inputValue = defaultText
      mixedOptions.text = message || mixedOptions.text
      mixedOptions.type = type || mixedOptions.type
      mixedOptions.showCancelButton = true
      mixedOptions.input = mixedOptions.input || 'text'
      Swal.fire(mixedOptions)
        .then(function (r) {
          if (r.value) {
            resolve(r.value)
          } else {
            reject(new Error('Could not fire sweetalert2'))
          }
        })
        .catch(function () {
          return reject(new Error('Could not fire sweetalert2'))
        })
    })
  }

  VueSimpleAlert.fire = function (options) {
    return Swal.fire(options)
  }

  VueSimpleAlert.Swal_close = function () {
    return Swal.close()
  }

  VueSimpleAlert.showValidationMessage = function (options) {
    return Swal.showValidationMessage(options)
  }

  VueSimpleAlert.install = function (Vue, options) {
    VueSimpleAlert.globalOptions = options
    Vue.alert = VueSimpleAlert.alert
    Vue.confirm = VueSimpleAlert.confirm
    Vue.prompt = VueSimpleAlert.prompt
    Vue.fire = VueSimpleAlert.fire
    Vue.Swal_close = VueSimpleAlert.Swal_close
    if (!Vue.prototype.hasOwnProperty('$alert')) {
      Vue.prototype.$alert = VueSimpleAlert.alert
    }
    if (!Vue.prototype.hasOwnProperty('$confirm')) {
      Vue.prototype.$confirm = VueSimpleAlert.confirm
    }
    if (!Vue.prototype.hasOwnProperty('$prompt')) {
      Vue.prototype.$prompt = VueSimpleAlert.prompt
    }
    if (!Vue.prototype.hasOwnProperty('$fire')) {
      Vue.prototype.$fire = VueSimpleAlert.fire
    }
    if (!Vue.prototype.hasOwnProperty('Swal_close')) {
      Vue.prototype.$Swal_close = VueSimpleAlert.Swal_close
    }
    if (!Vue.prototype.hasOwnProperty('$showValidationMessage')) {
      Vue.prototype.$showValidationMessage = VueSimpleAlert.showValidationMessage
    }
  }
  return VueSimpleAlert
}())

Vue.use(VueSimpleAlert)
export { VueSimpleAlert }
export default VueSimpleAlert
