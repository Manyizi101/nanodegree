deepdyve = {
    divId: '',
    divIdList: [],
    docId: '',
    fieldName: 'journal_mjid',
    rentText: 'Rent at DeepDyve',
    divIdMap: {},
    affiliateId: 'test',
    host: 'www.deepdyve.com',

    insertRentalLink: function() {
		deepdyve.getScript('http://' + deepdyve.host + '/rental-link?docId=' + deepdyve.docId + '&fieldName=' + deepdyve.fieldName + '&key=' + encodeURIComponent(deepdyve.affiliateId) + '&referrer=' + encodeURIComponent(location.href));
    },

    updateDiv: function(response, price) {
        if (!isEmpty(deepdyve.divIdMap)) {
            for (var i in deepdyve.divIdMap) {
                if (!response) {
                    var element = document.getElementById(i);
                    if (element) {
                        element.innerHTML = '';
                    }
                } else {
                    var anchorText = deepdyve.divIdMap[i];
                    if (price) {
                        anchorText = anchorText.replace('$price', '$' + price);
                    }
                    var element = document.getElementById(i)
                    if (element) {
                        element.innerHTML = '<a href="' + response + '&affiliate_link=default&referrer=' + encodeURIComponent(location.href) + '">' + anchorText + '</a>';
                    }
                }
            }
        } else {
            if (deepdyve.divId) {
                deepdyve.divIdList.push(deepdyve.divId);
            }
            for (var i in deepdyve.divIdList) {
                if (!response) {
                    var element = document.getElementById(deepdyve.divIdList[i]);
                    if (element) {
                        element.innerHTML = '';
                    }
                } else {
                    var anchorText = deepdyve.rentText;
                    if (price) {
                        anchorText = anchorText.replace('$price', '$' + price);
                    }
                    var element = document.getElementById(deepdyve.divIdList[i])
                    if(element) {
                        element.innerHTML = '<a href="' + response + '&affiliate_link=default&referrer=' + encodeURIComponent(location.href) + '">' + anchorText + '</a>';
                    }
                }
            }
        }
    },

	getScript: function(scriptFile) {
        var newScript = document.createElement('script');
        newScript.type = 'text/javascript';
        newScript.src = scriptFile;
		if (typeof scriptFile!="undefined")
			document.getElementsByTagName('head')[0].appendChild(newScript);
	},

    addEvent: function(obj, eventType, fn) {
        if (obj.addEventListener) {
            obj.addEventListener(eventType, fn, false);
            return true;
        } else if (obj.attachEvent) {
            var r = obj.attachEvent('on' + eventType, fn);
            return r;
        } else {
            return false;
        }
    }

}

function isEmpty(map) {
   for(var key in map) {
      if (map.hasOwnProperty(key)) {
         return false;
      }
   }
   return true;
}

deepdyve.addEvent(window, 'load', deepdyve.insertRentalLink);
