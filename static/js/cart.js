$(document).ready(function(){
    console.log("Hello")
    $(".update-cart").click(function(e){
        e.preventDefault()
        var id = $(this).data("product")
        var action = $(this).data("action")
        console.log(id)
        console.log(action)

        console.log("User: ", user)
        if (user === 'AnonymousUser'){
            addcookieitem(id, action)
           
        }else{
            updateCart(id, action)
        }
    })

    function updateCart(productid, action){
        console.log("Logged in sending data...")
        $.ajax({
            method: "POST",
            url: "update_item",
            data:{
                "product_id": productid,
                "action": action,
                csrfmiddlewaretoken: $("input[name = csrfmiddlewaretoken]").val(),
            },
            success: function(response){
                console.log(response)
                location.reload()
            }

        })
    }

    function addcookieitem(id, action){
        console.log("Not logged in...")
        if(action == "Add"){
            if(cart[id] == undefined){
                cart[id] = {"quantity":1}
            }else{
                cart[id]["quantity"] += 1
            }

        }
        if(action == "Remove"){
            cart[id]["quantity"] -= 1
            if(cart[id]["quantity"] <= 0){
                console.log("Remove item")

                delete cart[id]
            }
        }

        console.log("Cart:", cart)
        document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/"
        location.reload()
    }

    $(".fa-bars").click(function(){
        $('.link-bar').toggleClass('active')
    })
})