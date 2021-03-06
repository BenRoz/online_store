var Store = {};

Store.start = function(){
	$(document).ready(function() {
		Store.loadCategories();
		Store.loadStoreName_and_email();
	});
};

Store.loadCategories = function(){
	$.get("/categories",function(result){
			if (result["STATUS"] == "ERROR"){
				alert(result["MSG"]);
			}else{
				var categories = result["CATEGORIES"];
				var categoriesHolder = $("#categories");
				categoriesHolder.empty();
				for (i in categories){
					var categoryBtn = $("<nav />").addClass("nav-btn clickable").text(categories[i].name);
					categoryBtn.attr("id","cat-" + categories[i].id);
					categoryBtn.click(function(e){
						Store.loadProducts($(this).attr("id"));
					});
					categoriesHolder.append(categoryBtn)
				}
				$("#page").addClass("ready");
				var firstCategory = $("#categories .nav-btn").attr("id");
				Store.loadProducts(firstCategory);
			}
		},"json");
};

Store.loadProducts = function(category){
	var categoryID = category.replace("cat-","");
	$.get("/category/" + categoryID + "/products",function(result){
		$("#content").empty();
		for( i in result["PRODUCTS"]){
			var productObj = result["PRODUCTS"][i];
			var product = $("#templates .product").clone();
			product.find(".img").css("background-image","url('"+ productObj.img_url +"')");
			product.find(".title").text(productObj.title);
			product.find(".desc").text(productObj.description);
			product.find(".price").text("$" + productObj.price);
			product.find("form input[name='item_name']").val(productObj.title);
			product.find("form input[name='item_number']").val(productObj.id);
			product.find("form input[name='amount']").val(productObj.price);
			if (productObj.favorite){
				product.addClass("favorite");
			}
			$("#content").append(product);
		}
	},"json");
};

Store.loadStoreName_and_email= function(){
	$.get("/fetching_settings",function(result){
			if (result["STATUS"] == "ERROR"){
				alert(result["MSG"]);
			}else{
				var selected_store_name = result["NAME"][0]["name"];
				$(".store_name").text(selected_store_name);
				var email_address = result["EMAIL"]["name"];
                $("#email_field").val(email_address);
            }
		},"json");
};

var admin_button = $("#admin_btn");
admin_button.click(function(){
    $.get("/admin",function(){
				console.log ("hope");
		},"json");
});

Store.to_admin = function(){
    window.location.assign("http://localhost:7008/admin")
};

Store.start();

