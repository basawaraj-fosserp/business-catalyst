console.log("Hello gelllo")

webshop.ProductList = class extends webshop.ProductList {
    get_image_html(item, title, settings) {
        console.log("Enter With")
		let image = item.website_image;
		let wishlist_enabled = !item.has_variants && settings.enable_wishlist;
		let image_html = ``;
		// if (image) {
		// 	image_html += `
		// 		<div class="col-2 border text-center rounded list-image">
		// 			<a class="product-link product-list-link" href="/${ item.route || '#' }">
		// 				<img itemprop="image" class="website-image h-100 w-100" alt="${ title }"
		// 					src="${ image }">
		// 			</a>
		// 			${ wishlist_enabled ? this.get_wishlist_icon(item): '' }
		// 		</div>
		// 	`;
		// } else {
		// 	image_html += `
		// 		<div class="col-2 border text-center rounded list-image">
		// 			<a class="product-link product-list-link" href="/${ item.route || '#' }"
		// 				style="text-decoration: none">
		// 				<div class="card-img-top no-image-list">
		// 					${ frappe.get_abbr(title) }
		// 				</div>
		// 			</a>
		// 			${ wishlist_enabled ? this.get_wishlist_icon(item): '' }
		// 		</div>
		// 	`;
		// }

		return image_html;
	}
}