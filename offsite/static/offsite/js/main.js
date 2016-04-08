/**
 *  created by Gudach Ilia
 */

(function () {
	// using jQuery
	getCookie = function(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');
	// удаление объекта
	delete_object = function(element) {
		$.ajax({
	        url : element.href,
	        type : "DELETE",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(json) {
	        	console.log(json);
	        	if (json.status == 'success') {
	        		$(element).parent().remove();
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
	
	$( document ).ready(function() {
		// удаление
		$('.delete').on('click', function(event){
		    event.preventDefault();
		    delete_object(this);
		});
		// загрузка файлов
		$('form.auth').on('change', '#addimage', function(event){
			var files = event.target.files;
			upload_files(files);
		});
		// удаление файлов
		$('form.auth').on('click', '.delete-row', function(event) {
			event.preventDefault();
			delete_file(this);
		});
		// получение списка объектов
		$('form.auth').on('click', '.get-objects', function(event) {
			event.preventDefault();
			get_objects(this);
		});
		// прикрепление к объекту
		$('form.auth').on('click', '.join-object', function(event) {
			event.preventDefault();
			join_object(this);
		});
		// получение списка прикреплённых объектов
		$('form.auth').on('click', '.get-joined-objects', function(event) {
			event.preventDefault();
			get_joined_objects(this);
		});
		// открепление от объекта
		$('form.auth').on('click', '.unjoin-object', function(event) {
			event.preventDefault();
			unjoin_object(this);
		});
		// получение списка объектов
		$('form.auth').on('click', '.get-objects-for-title-photo', function(event) {
			event.preventDefault();
			get_objects_for_title_photo(this);
		});
		// установление главной фото для объкта
		$('form.auth').on('click', '.title-photo', function(event) {
			event.preventDefault();
			make_title_photo(this);
		});
		// установление главной фото для печника
		$('form.auth').on('click', '.set-photo-for-ovenbird', function(event) {
			event.preventDefault();
			set_photo_for_ovenbird(this);
		});
		// присоединение или отсоединение от объекта
		$('form.auth').on('change', '.check-photo', function(event) {
			if (this.checked) {
				join_object2(this);
			} else {
				unjoin_object2(this);
			}
		});
		// получение фото для выбранного объекта
		$('form.auth').on('click', '.get-photos', function(event) {
			event.preventDefault();
			get_photos(this);
		});
	});
	// удаление файла
	delete_file = function(element) {
		$.ajax({
	        url : element.href,
	        type : "DELETE",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	console.log(response);
	        	if (response.status == 'success') {
	        		$(element).parent().remove();
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
	// загрузка файлов
	upload_files = function(files) {
		for (var i = 0; i < files.length; i++) {
			var data = new FormData();
			data.append('image', files[i])
			$.ajax({
				url : '/offsite/File/Add/',
				type : "POST",
				xhr: function() {
					var myXhr = $.ajaxSettings.xhr();
					if(myXhr.upload){
						myXhr.upload.addEventListener('progress',progressHandlingFunction, false);
					}
					return myXhr;
				},
				beforeSend: function (request) {
					request.setRequestHeader("X-CSRFToken", csrftoken);
				},
				success : function(json) {
					photo = JSON.parse(json.photo);
					if (json.status == 'success') {
						element = $('#id_empty_form').clone()
							.appendTo('form')
							.after()
							.show();
						new_src = element.find('img')
							.attr('name')+photo[0].fields.image;
						element.find('img')
							.attr('src', new_src);
						a_link = element.find('a')
							.attr('href');
						element.find('a')
							.attr('href',a_link.replace(0, photo[0].pk));
					}
				},
				error : function(xhr,errmsg,err) {
					console.log(xhr.status + ": " + xhr.responseText);
				},
				data: data,
				cache: false,
				contentType: false,
				processData: false
			});
		}
	}
	function progressHandlingFunction(e){
	    if(e.lengthComputable){
	        $('progress').attr({value:e.loaded,max:e.total});
	    }
	}
	//  получает список объектов или статей
	get_objects = function(element) {
		$.ajax({
	        url : element.href,
	        type : "GET",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	if (response.status == 'success' && response.objects) {
		        	var str = '';
		        	fields = jQuery.parseJSON(response.objects);
	        		for (var i = 0; i < fields.length; i++) {
	        			str += '<a class="join-object" href="/offsite/JoinObject/' 
	        				+ $(element).attr('id') + '/' + fields[i].pk + '/">' + fields[i].fields.title + '<br/>';
	        		}
	        		if (str === '') {
	        			str = 'У вас нет объектов или статей';
	        		}
	        		$(element).next().html(str);
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
	// прикрепляет файл к объекту или статье
	join_object = function(element) {
		$.ajax({
	        url : element.href,
	        type : "POST",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	if (response.status == 'success') {
	        		console.log($(element).parent());
	        		$(element).parent()
						.html('');
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
	//  получает список прикреплённых объектов
	get_joined_objects = function(element) {
		$.ajax({
	        url : element.href,
	        type : "GET",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	if (response.status == 'success' && response.objects) {
	        		var str = '';
		        	fields = jQuery.parseJSON(response.objects);
	        		for (var i = 0; i < fields.length; i++) {
	        			str += '<a class="unjoin-object" href="/offsite/UnjoinObject/' 
	        				+ $(element).attr('id') + '/' + fields[i].pk + '/">' + fields[i].fields.title + '<br/>';
	        		}
	        		if (str === '') {
	        			str = 'У вас нет прикреплённых объектов или статей';
	        		}
	        		$(element).next().html(str);
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}	
	// отделяет файл от объекта или статьи
	unjoin_object = function(element) {
		$.ajax({
	        url : element.href,
	        type : "POST",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	if (response.status == 'success') {
	        		console.log($(element).parent());
	        		$(element).parent()
						.html('');
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
	get_objects_for_title_photo = function(element) {
		$.ajax({
	        url : element.href,
	        type : "GET",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	if (response.status == 'success' && response.objects) {
		        	var str = '';
		        	fields = jQuery.parseJSON(response.objects);
	        		for (var i = 0; i < fields.length; i++) {
	        			str += '<a class="title-photo" href="/offsite/MakeTitlePhoto/'
	        				+ $(element).attr('id') + '/' + fields[i].pk + '/">' + fields[i].fields.title + '<br/>';
	        		}
	        		if (str === '') {
	        			str = 'У вас нет объектов или статей';
	        		}
	        		$(element).next().html(str);
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
	// делает фотографию главной для объекта
	make_title_photo = function(element) {
		$.ajax({
	        url : element.href,
	        type : "POST",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	if (response.status == 'success') {
	        		$(element).parent()
						.html('');
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
	// делает фотографию главной для печника
	set_photo_for_ovenbird = function(element) {
		$.ajax({
	        url : element.href,
	        type : "POST",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	if (response.status == 'success') {
	        		
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
	// отделяет файл от объекта или статьи
	unjoin_object2 = function(element) {
		$.ajax({
	        url : '/offsite/File/UnjoinObject/'+element.id+'/',
	        type : "POST",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	if (response.status == 'success') {
	        		
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
	// отделяет файл от объекта или статьи
	join_object2 = function(element) {
		$.ajax({
	        url : '/offsite/File/JoinObject/'+element.id+'/',
	        type : "POST",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	if (response.status == 'success') {
	        		
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
	// получает все фотографии для объекта 
	get_photos = function(element) {
		$.ajax({
	        url : element.href,
	        type : "GET",
	        beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
	        success : function(response) {
	        	console.log(response.objects);
	        	if (response.status == 'success' && response.objects) {
		        	// после нажатия снова и снова будет вставлять фотографии
		        	fields = jQuery.parseJSON(response.objects);
	        		for (var i = 0; i < fields.length; i++) {
	        			clone = $('#id_empty_form').clone()
							.insertAfter($(element))
							.show();
	        			$(clone).children()[0].id = $(clone).children()[0].id.replace('0', fields[i].pk);
	        			$(clone).children()[1].src = $(clone).children()[1].name+fields[i].fields.image;
	        		}
	        	}
	        },
	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
	}
})();