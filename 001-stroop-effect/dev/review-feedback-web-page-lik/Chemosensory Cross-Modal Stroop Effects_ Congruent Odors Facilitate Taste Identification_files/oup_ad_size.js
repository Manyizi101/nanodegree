/**
 * @file
 *
 * The OUP advert script.
 */
var OUP_Advert = {
	// ID prefix to search.
	idPrefix: 'oas_',
	// Available advert sizes.
	sizes: {
		//Top1: [728, 90],
		Top: [728, 90],
		Right1: [160, 600],
		Right2: [160, 600],
		Bottom: [728, 90]
	},
	// Add JS file.
	AddScript: function(URI) {
		var oupcat = document.createElement('script');
		var protocol = 'https:' == document.location.protocol ? 'https://' : 'http://';
		var node = document.getElementsByTagName('script')[0];
		oupcat.type = 'text/javascript';
		oupcat.async = true;
		oupcat.src = protocol + URI;
		node.parentNode.insertBefore(oupcat, node);
	}
};

OUP_Advert.AddScript('www.oxfordjournals.org/resource/js/caturls.js');
// oas_tag used by real media JS.
var oas_tag = {
	// Define OAS URL.
	url: 'oas.oxfordjournals.org',
	// Define OAS Site page.
	site_page: 'www.async-tag.com',
	// Define Keywords.
	query: 'keyword',
	analytics: true,
	taxonomy: 'user=1234',
	version: '1',
	logging: true,
	allowSizeOverride: true,
	// Collect the slot list, (enabled / disabled slots).
	sizes: function() {
		// Find all div's that begin with our advert prefix.
		var $oupAdvertDivs = jQuery('div[id^="' + OUP_Advert.idPrefix + '"]');

		var slotList = [];
		$oupAdvertDivs.each(function() {
			var advertID = jQuery(this).attr('id');
			var advertName = advertID.replace(OUP_Advert.idPrefix, '');
			var advertNameN = advertName.charAt(0).toUpperCase() + advertName.substring(1);
			if(OUP_Advert.sizes[advertNameN] === undefined) {
				jQuery(this).remove();
			} else {
				// Check if this ID is enabled from the Categorizer script.
				if (window.Categorizer ? Categorizer(advertID) : true) {
					// fix ID
					jQuery(this).attr('id', OUP_Advert.idPrefix + advertNameN)
					jQuery(this).attr('class', '');
					jQuery(this).empty();
					jQuery(this).css({
						'clear': 'both',
						'text-align': 'center',
						'margin-bottom': '16px'
					});
					//oas_tag.site_page = window.Categorize ? window.Categorize(window.location) : (window.location.hostname + window.location.pathname);
					oas_tag.site_page = window.Categorize ? window.Categorize(window.location.hostname + window.location.pathname) : (window.location.hostname + window.location.pathname);
					// Define pos is added by real media, which calls sizes, so this should
					// always be defined as a function.
					if (typeof oas_tag.definePos == "function") {
						oas_tag.definePos(advertNameN, OUP_Advert.sizes[advertNameN]);
						slotList.push(advertID);
					};
				};
			};
		});
		return slotList;
	}
};

// Add advert launcher on 'document ready' function.

function init_oas() {
	if (window.jQuery) {
		jQuery(document).ready(function() {
			OUP_Advert.AddScript(oas_tag.url + '/om/' + oas_tag.version + '.js');
		});
	} else {
		setTimeout(init_oas, 100);
	}
}

init_oas();
