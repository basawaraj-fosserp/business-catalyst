(() => {
  // ../business_catalyst/business_catalyst/public/js/product_ui/list.js
  console.log("Hello gelllo");
  webshop.ProductList = class extends webshop.ProductList {
    get_image_html(item, title, settings) {
      console.log("Enter With");
      let image = item.website_image;
      let wishlist_enabled = !item.has_variants && settings.enable_wishlist;
      let image_html = ``;
      return image_html;
    }
  };
})();
//# sourceMappingURL=business_catalyst.bundle.D6UN7BXO.js.map
