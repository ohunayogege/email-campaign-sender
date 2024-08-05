/*
Template: EmailCHIMP
Author: BITBIZ NG
Design and Developed by: BITBIZ NG
NOTE: This file contains the styling for responsive Template.
*/

/*----------------------------------------------
Index Of Script
------------------------------------------------

:: Tooltip
:: Fixed Nav
:: Magnific Popup
:: Ripple Effect
:: Sidebar Widget
:: FullScreen
:: Page Loader
:: Counter
:: Progress Bar
:: Page Menu
:: Close  navbar Toggle
:: Mailbox
:: chatuser
:: chatuser main
:: Chat start
:: todo Page
:: user toggle
:: Data tables
:: Form Validation
:: Active Class for Pricing Table
:: Flatpicker
:: Scrollbar
:: checkout
:: Datatables
:: image-upload
:: video
:: Button
:: Pricing tab
:: List And Grid
:: Create User
:: Login

------------------------------------------------
Index Of Script
----------------------------------------------*/

(function(jQuery) {

    "use strict";
    jQuery(document).ready(function() {

        /*---------------------------------------------------------------------
        Tooltip
        -----------------------------------------------------------------------*/
        jQuery('[data-toggle="popover"]').popover();
        jQuery('[data-toggle="tooltip"]').tooltip();

        /*---------------------------------------------------------------------
        Fixed Nav
        -----------------------------------------------------------------------*/

        $(window).on('scroll', function() {
            if ($(window).scrollTop() > 0) {
                $('.iq-top-navbar').addClass('fixed');
            } else {
                $('.iq-top-navbar').removeClass('fixed');
            }
        });

        $(window).on('scroll', function() {
            if ($(window).scrollTop() > 0) {
                $('.white-bg-menu').addClass('sticky-menu');
            } else {
                $('.white-bg-menu').removeClass('sticky-menu');
            }
        });


        /*---------------------------------------------------------------------
        Magnific Popup
        -----------------------------------------------------------------------*/
        if (typeof $.fn.magnificPopup !== typeof undefined) {
            jQuery('.popup-gallery').magnificPopup({
                delegate: 'a.popup-img',
                type: 'image',
                tLoading: 'Loading image #%curr%...',
                mainClass: 'mfp-img-mobile',
                gallery: {
                    enabled: true,
                    navigateByImgClick: true,
                    preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
                },
                image: {
                    tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
                    titleSrc: function(item) {
                        return item.el.attr('title') + '<small>by Marsel Van Oosten</small>';
                    }
                }
            });
            jQuery('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
                disableOn: 700,
                type: 'iframe',
                mainClass: 'mfp-fade',
                removalDelay: 160,
                preloader: false,
                fixedContentPos: false
            });
        }


        /*---------------------------------------------------------------------
        Ripple Effect
        -----------------------------------------------------------------------*/
        jQuery(document).on('click', ".iq-waves-effect", function(e) {
            // Remove any old one
            jQuery('.ripple').remove();
            // Setup
            let posX = jQuery(this).offset().left,
                posY = jQuery(this).offset().top,
                buttonWidth = jQuery(this).width(),
                buttonHeight = jQuery(this).height();

            // Add the element
            jQuery(this).prepend("<span class='ripple'></span>");


            // Make it round!
            if (buttonWidth >= buttonHeight) {
                buttonHeight = buttonWidth;
            } else {
                buttonWidth = buttonHeight;
            }

            // Get the center of the element
            let x = e.pageX - posX - buttonWidth / 2;
            let y = e.pageY - posY - buttonHeight / 2;


            // Add the ripples CSS and start the animation
            jQuery(".ripple").css({
                width: buttonWidth,
                height: buttonHeight,
                top: y + 'px',
                left: x + 'px'
            }).addClass("rippleEffect");
        });

        /*---------------------------------------------------------------------
         Sidebar Widget
         -----------------------------------------------------------------------*/

        jQuery(document).on("click", '.iq-menu > li > a', function() {
            jQuery('.iq-menu > li > a').parent().removeClass('active');
            jQuery(this).parent().addClass('active');
        });

        // Active menu
        var parents = jQuery('li.active').parents('.iq-submenu.collapse');

        parents.addClass('show');


        parents.parents('li').addClass('active');
        jQuery('li.active > a[aria-expanded="false"]').attr('aria-expanded', 'true');

        /*---------------------------------------------------------------------
        FullScreen
        -----------------------------------------------------------------------*/
        jQuery(document).on('click', '.iq-full-screen', function() {
            let elem = jQuery(this);
            if (!document.fullscreenElement &&
                !document.mozFullScreenElement && // Mozilla
                !document.webkitFullscreenElement && // Webkit-Browser
                !document.msFullscreenElement) { // MS IE ab version 11

                if (document.documentElement.requestFullscreen) {
                    document.documentElement.requestFullscreen();
                } else if (document.documentElement.mozRequestFullScreen) {
                    document.documentElement.mozRequestFullScreen();
                } else if (document.documentElement.webkitRequestFullscreen) {
                    document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
                } else if (document.documentElement.msRequestFullscreen) {
                    document.documentElement.msRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
                }
            } else {
                if (document.cancelFullScreen) {
                    document.cancelFullScreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.webkitCancelFullScreen) {
                    document.webkitCancelFullScreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
            }
            elem.find('i').toggleClass('ri-fullscreen-line').toggleClass('ri-fullscreen-exit-line');
        });


        /*---------------------------------------------------------------------
        Page Loader
        -----------------------------------------------------------------------*/
        jQuery("#load").fadeOut();
        jQuery("#loading").delay().fadeOut("");


        /*---------------------------------------------------------------------
        Counter
        -----------------------------------------------------------------------*/
        if (window.counterUp !== undefined) {
            const counterUp = window.counterUp["default"]
            const $counters = $(".counter");
            $counters.each(function(ignore, counter) {
                var waypoint = new Waypoint({
                    element: $(this),
                    handler: function() {
                        counterUp(counter, {
                            duration: 1000,
                            delay: 10
                        });
                        this.destroy();
                    },
                    offset: 'bottom-in-view',
                });
            });
        }


        /*---------------------------------------------------------------------
        Progress Bar
        -----------------------------------------------------------------------*/
        jQuery('.iq-progress-bar > span').each(function() {
            let progressBar = jQuery(this);
            let width = jQuery(this).data('percent');
            progressBar.css({
                'transition': 'width 2s'
            });

            setTimeout(function() {
                progressBar.appear(function() {
                    progressBar.css('width', width + '%');
                });
            }, 100);
        });

        jQuery('.progress-bar-vertical > span').each(function() {
            let progressBar = jQuery(this);
            let height = jQuery(this).data('percent');
            progressBar.css({
                'transition': 'height 2s'
            });
            setTimeout(function() {
                progressBar.appear(function() {
                    progressBar.css('height', height + '%');
                });
            }, 100);
        });



        /*---------------------------------------------------------------------
        Page Menu
        -----------------------------------------------------------------------*/
        jQuery(document).on('click', '.wrapper-menu', function() {
            jQuery(this).toggleClass('open');
        });

        jQuery(document).on('click', ".wrapper-menu", function() {
            jQuery("body").toggleClass("sidebar-main");
        });


        /*---------------------------------------------------------------------
         Close  navbar Toggle
         -----------------------------------------------------------------------*/

        jQuery('.close-toggle').on('click', function() {
            jQuery('.h-collapse.navbar-collapse').collapse('hide');
        });


        /*---------------------------------------------------------------------
        Mailbox
        -----------------------------------------------------------------------*/
        jQuery(document).on('click', 'ul.iq-email-sender-list li', function() {
            jQuery(this).next().addClass('show');
            // jQuery('.mail-box-detail').css('filter','blur(4px)');
        });

        jQuery(document).on('click', '.email-app-details li h4', function() {
            jQuery('.email-app-details').removeClass('show');
        });

        /*---------------------------------------------------------------------
        chatuser
        -----------------------------------------------------------------------*/
        jQuery(document).on('click', '.chat-head .chat-user-profile', function() {
            jQuery(this).parent().next().toggleClass('show');
        });
        jQuery(document).on('click', '.user-profile .close-popup', function() {
            jQuery(this).parent().parent().removeClass('show');
        });

        /*---------------------------------------------------------------------
        chatuser main
        -----------------------------------------------------------------------*/
        jQuery(document).on('click', '.chat-search .chat-profile', function() {
            jQuery(this).parent().next().toggleClass('show');
        });
        jQuery(document).on('click', '.user-profile .close-popup', function() {
            jQuery(this).parent().parent().removeClass('show');
        });

        /*---------------------------------------------------------------------
        Chat start
        -----------------------------------------------------------------------*/
        jQuery(document).on('click', '#chat-start', function() {
            jQuery('.chat-data-left').toggleClass('show');
        });
        jQuery(document).on('click', '.close-btn-res', function() {
            jQuery('.chat-data-left').removeClass('show');
        });
        jQuery(document).on('click', '.iq-chat-ui li', function() {
            jQuery('.chat-data-left').removeClass('show');
        });
        jQuery(document).on('click', '.sidebar-toggle', function() {
            jQuery('.chat-data-left').addClass('show');
        });

        /*---------------------------------------------------------------------
        todo Page
        -----------------------------------------------------------------------*/
        jQuery(document).on('click', '.todo-task-list > li > a', function() {
            jQuery('.todo-task-list li').removeClass('active');
            jQuery('.todo-task-list .sub-task').removeClass('show');
            jQuery(this).parent().toggleClass('active');
            jQuery(this).next().toggleClass('show');
        });
        jQuery(document).on('click', '.todo-task-list > li li > a', function() {
            jQuery('.todo-task-list li li').removeClass('active');
            jQuery(this).parent().toggleClass('active');
        });

        /*---------------------------------------------------------------------
        user toggle
        -----------------------------------------------------------------------*/
        jQuery(document).on('click', '.iq-user-toggle', function() {
            jQuery(this).parent().addClass('show-data');
        });

        jQuery(document).on('click', ".close-data", function() {
            jQuery('.iq-user-toggle').parent().removeClass('show-data');
        });
        jQuery(document).on("click", function(event) {
            var $trigger = jQuery(".iq-user-toggle");
            if ($trigger !== event.target && !$trigger.has(event.target).length) {
                jQuery(".iq-user-toggle").parent().removeClass('show-data');
            }
        });
        /*-------hide profile when scrolling--------*/
        jQuery(window).scroll(function() {
            let scroll = jQuery(window).scrollTop();
            if (scroll >= 10 && jQuery(".iq-user-toggle").parent().hasClass("show-data")) {
                jQuery(".iq-user-toggle").parent().removeClass("show-data");
            }
        });
        let Scrollbar = window.Scrollbar;
        if (jQuery('.data-scrollbar').length) {
            Scrollbar.init(document.querySelector('.data-scrollbar'), { continuousScrolling: false });
        }

        // Index List
        if (jQuery('.index-list-scrollbar').length) {
            Scrollbar.init(document.querySelector('.index-list-scrollbar'), { continuousScrolling: false });
        }


        /*---------------------------------------------------------------------
        Data tables
        -----------------------------------------------------------------------*/
        if ($.fn.DataTable) {
            $('.data-table').DataTable();
        }




        /*---------------------------------------------------------------------
        Form Validation
        -----------------------------------------------------------------------*/

        // Example starter JavaScript for disabling form submissions if there are invalid fields
        window.addEventListener('load', function() {
            // Fetch all the forms we want to apply custom Bootstrap validation styles to
            var forms = document.getElementsByClassName('needs-validation');
            // Loop over them and prevent submission
            var validation = Array.prototype.filter.call(forms, function(form) {
                form.addEventListener('submit', function(event) {
                    if (form.checkValidity() === false) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                }, false);
            });
        }, false);

        /*---------------------------------------------------------------------
         Active Class for Pricing Table
         -----------------------------------------------------------------------*/
        jQuery("#my-table tr th").click(function() {
            jQuery('#my-table tr th').children().removeClass('active');
            jQuery(this).children().addClass('active');
            jQuery("#my-table td").each(function() {
                if (jQuery(this).hasClass('active')) {
                    jQuery(this).removeClass('active')
                }
            });
            var col = jQuery(this).index();
            jQuery("#my-table tr td:nth-child(" + parseInt(col + 1) + ")").addClass('active');
        });

        /*------------------------------------------------------------------
        Flatpicker
        * -----------------------------------------------------------------*/
        if (jQuery('.date-input').hasClass('basicFlatpickr')) {
            jQuery('.basicFlatpickr').flatpickr();
            jQuery('#inputTime').flatpickr({
                enableTime: true,
                noCalendar: true,
                dateFormat: "H:i",
            });
            jQuery('#inputDatetime').flatpickr({
                enableTime: true
            });
            jQuery('#inputWeek').flatpickr({
                weekNumbers: true
            });
            jQuery("#inline-date").flatpickr({
                inline: true
            });
            jQuery("#inline-date1").flatpickr({
                inline: true
            });
        }

        /*---------------------------------------------------------------------
        Scrollbar
        -----------------------------------------------------------------------*/

        jQuery(window).on("resize", function() {
            if (jQuery(this).width() <= 1299) {
                jQuery('#salon-scrollbar').addClass('data-scrollbar');
            } else {
                jQuery('#salon-scrollbar').removeClass('data-scrollbar');
            }
        }).trigger('resize');

        jQuery('.data-scrollbar').each(function() {
            var attr = $(this).attr('data-scroll');
            if (typeof attr !== typeof undefined && attr !== false) {
                let Scrollbar = window.Scrollbar;
                var a = jQuery(this).data('scroll');
                Scrollbar.init(document.querySelector('div[data-scroll= "' + a + '"]'));
            }
        });


        /*---------------------------------------------------------------------
           Datatables
        -----------------------------------------------------------------------*/
        if (jQuery('.data-tables').length) {
            $('.data-tables').DataTable();
        }


        /*---------------------------------------------------------------------
        image-upload
        -----------------------------------------------------------------------*/

        $('.form_gallery-upload').on('change', function() {
            var length = $(this).get(0).files.length;
            var galleryLabel = $(this).attr('data-name');

            if (length > 1) {
                $(galleryLabel).text(length + " files selected");
            } else {
                $(galleryLabel).text($(this)[0].files[0].name);
            }
        });

        /*---------------------------------------------------------------------
            video
          -----------------------------------------------------------------------*/
        $(document).ready(function() {
            $('.form_video-upload input').change(function() {
                $('.form_video-upload p').text(this.files.length + " file(s) selected");
            });
        });


        /*---------------------------------------------------------------------
        Button
        -----------------------------------------------------------------------*/

        jQuery('.qty-btn').on('click', function() {
            var id = jQuery(this).attr('id');

            var val = parseInt(jQuery('#quantity').val());

            if (id == 'btn-minus') {
                if (val != 0) {
                    jQuery('#quantity').val(val - 1);
                } else {
                    jQuery('#quantity').val(0);
                }

            } else {
                jQuery('#quantity').val(val + 1);
            }
        });
        if ($.fn.select2 !== undefined) {
            $("#single").select2({
                placeholder: "Select a Option",
                allowClear: true
            });
            $("#multiple").select2({
                placeholder: "Select a Multiple Option",
                allowClear: true
            });
            $("#multiple2").select2({
                placeholder: "Select a Multiple Option",
                allowClear: true
            });
        }



        /*---------------------------------------------------------------------
        List
        -----------------------------------------------------------------------*/

        $('[data-toggle="pill"]').on('click', function() {
            const extra_hide = $(this).attr('data-hide');
            $(document).find('.tab-extra').removeClass('iq-hide');
            if (extra_hide !== undefined) {
                $(extra_hide).addClass('iq-hide');
            }
        })

        if ($('[data-placement="daterange"]').length) {
            $('[data-placement="daterange"]').daterangepicker({
                opens: 'center'
            }, function(start, end, label) {
                console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
            });
        }

        $('#view-event').on('click', function(e) {
            e.preventDefault()
            $('#view-btn').tab('show');
        })


        $(document).on('click', '[data-extra-toggle="copy"]', function(e) {
            e.preventDefault()
            $(this).attr("title", "Copied!").tooltip("_fixTitle").tooltip("show").attr("title", "Copy to clipboard").tooltip("_fixTitle");
            const input = $(this).data("input")
            copyToClipboard($(input).val())

        })

        $(document).on('click', '[data-extra-toggle="random-text"]', function(e) {
            e.preventDefault()
            const length = $(this).data('length')
            const input = $(this).data('input')
            const target = $(this).data('target')
            const value = random(length)
            $(input).val(value)
            $(target).html(value)
        })



        /*---------------------------------------------------------------------
        Pricing tab
        -----------------------------------------------------------------------*/
        jQuery(window).on('scroll', function(e) {

            // Pricing Pill Tab
            var nav = jQuery('#pricing-pills-tab');
            if (nav.length) {
                var contentNav = nav.offset().top - window.outerHeight;
                if (jQuery(window).scrollTop() >= (contentNav)) {
                    e.preventDefault();
                    jQuery('#pricing-pills-tab li a').removeClass('active');
                    jQuery('#pricing-pills-tab li a[aria-selected=true]').addClass('active');
                }
            }
        });

        /*---------- */
        $(".dropdown-menu li a").click(function() {
            var selHtml = $(this).html();
            var selName = $.trim($(this).text())
            $(this).parents('.btn-group').find('.search-replace').html(selHtml);
            $(this).parents('.btn-group').find('.search-query').val(selName);
        });

    });

    $("ul.nav-tabs a").click(function(e) {
        e.preventDefault();
        $(this).tab('show');
    });


    /*---------------------------------------------------------------------
      List and Grid
    -----------------------------------------------------------------------*/
    $('[data-extra-toggle="delete"]').on('click', function(e) {
        const closestElem = $(this).attr('data-closest-elem')
        const swalWithBootstrapButtons = Swal.mixin({
            customClass: {
                confirmButton: 'btn btn-primary btn-lg',
                cancelButton: 'btn btn-outline-primary btn-lg ml-2'
            },
            buttonsStyling: false
        })

        swalWithBootstrapButtons.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes, delete it!',
                showClass: {
                    popup: 'animate__animated animate__zoomIn'
                },
                hideClass: {
                    popup: 'animate__animated animate__zoomOut'
                }
            })
            .then((willDelete) => {
                if (willDelete.isConfirmed) {
                    swalWithBootstrapButtons.fire({
                        title: 'Deleted!',
                        text: "Your Email has been deleted.",
                        icon: 'success',
                        showClass: {
                            popup: 'animate__animated animate__zoomIn'
                        },
                        hideClass: {
                            popup: 'animate__animated animate__zoomOut'
                        }
                    }).then(() => {
                        if (closestElem == '.card') {
                            $(this).closest(closestElem).parent().remove()
                        } else {
                            $(this).closest(closestElem).remove()
                        }
                    })
                } else {
                    swalWithBootstrapButtons.fire({
                        title: "Your Email is safe!",
                        showClass: {
                            popup: 'animate__animated animate__zoomIn'
                        },
                        hideClass: {
                            popup: 'animate__animated animate__zoomOut'
                        }
                    });
                }
            });
    })


    $('#warning').on('click', function() {
        Swal.fire({
            icon: 'warning',
            title: 'Changes are not saved',
            showConfirmButton: false,

        })
    });

    $('#confirmation').on('click', function() {
        Swal.fire({
                title: "Are you sure?",
                text: "Once deleted, you will not be able to recover this imaginary file!",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((willDelete) => {
                if (willDelete) {
                    Swal.fire("Poof! Your imaginary file has been deleted!", {
                        icon: "success",
                    });
                } else {
                    Swal.fire("Your imaginary file is safe!");
                }
            });
    });

    $(".form-create-user").on("submit", function(e){
        e.preventDefault()
        const form = $(this);
        $.ajax({
          url: window.location.url,
          method: "POST",
          data: form.serialize(),
          type: "json",
          beforeSend: function () {
            $(".btn-create-user").attr("disabled", true);
            $(".btn-create-user").text("Please wait...");
          },
          complete: function () {
            $(".btn-create-user").attr("disabled", false);
            $(".btn-create-user").text("Proceed");
          },
          success: function (res) {
            if (res.status) {
              Swal.fire({
                title: "User created successfully",
                text: res.message,
                icon: "success",
                confirmButtonText: "Ok",
              }).then(() => {
                window.location.reload();
              });
            } else {
              Swal.fire({
                title: "Error",
                text: res.message,
                icon: "error",
                confirmButtonText: "Ok",
              });
            }
          },
        });
    });

    $(".form-login").on("submit", function (e) {
      e.preventDefault();
      const form = $(this);
      $.ajax({
        url: window.location.url,
        method: "POST",
        data: form.serialize(),
        type: "json",
        beforeSend: function () {
          $(".btn-login").attr("disabled", true);
          $(".btn-login").text("Please wait...");
        },
        complete: function () {
          $(".btn-login").attr("disabled", false);
          $(".btn-login").text("Login");
        },
        success: function (res) {
          if (res.status) {
            Swal.fire({
              title: "Login Success",
              text: res.message,
              icon: "success",
              confirmButtonText: "Ok",
            }).then(() => {
              window.location.reload();
            });
          } else {
            Swal.fire({
              title: "Login Error",
              text: res.message,
              icon: "error",
              confirmButtonText: "Ok",
            });
          }
        },
      });
    });

    $(".form-segment").on("submit", function (e) {
      e.preventDefault();
      const form = $(this);
      $.ajax({
        url: window.location.url,
        method: "POST",
        data: form.serialize(),
        type: "json",
        beforeSend: function () {
          $(".btn-segment").attr("disabled", true);
          $(".btn-segment").text("Please wait...");
        },
        complete: function () {
          $(".btn-segment").attr("disabled", false);
          $(".btn-segment").text("Save Segment");
        },
        success: function (res) {
          if (res.status) {
            Swal.fire({
              title: "Saving Success",
              text: res.message,
              icon: "success",
              confirmButtonText: "Ok",
            }).then(() => {
              window.location.href = "/contacts/";
            });
          } else {
            Swal.fire({
              title: "Segment Error",
              text: res.message,
              icon: "error",
              confirmButtonText: "Ok",
            });
          }
        },
        error: function (err) {
          Swal.fire({
            title: "Server Error",
            text: "An error occurred while saving the segment",
            icon: "error",  
            confirmButtonText: "Ok",
          });
        },
      });
    });

    $(".form-contact").on("submit", function (e) {
      e.preventDefault();
      const form = $(this);
      $.ajax({
        url: window.location.url,
        method: "POST",
        data: form.serialize(),
        type: "json",
        beforeSend: function () {
          $(".btn-save-contact").attr("disabled", true);
          $(".btn-save-contact").text("Please wait...");
        },
        complete: function () {
          $(".btn-save-contact").attr("disabled", false);
          $(".btn-save-contact").text("Save Contact");
        },
        success: function (res) {
          if (res.status) {
            Swal.fire({
              title: "Saving Success",
              text: res.message,
              icon: "success",
              confirmButtonText: "Ok",
            }).then(() => {
              window.location.href = "/contacts/";
            });
          } else {
            Swal.fire({
              title: "Contact Error",
              text: res.message,
              icon: "error",
              confirmButtonText: "Ok",
            });
          }
        },
        error: function (err) {
          Swal.fire({
            title: "Server Error",
            text: "An error occurred while saving the contact",
            icon: "error",
            confirmButtonText: "Ok",
          });
        },
      });
    });

    const uploadForm = document.getElementById("upload_form");
    const input_file = document.getElementById("id_image");
    const progress_bar = document.getElementById("progress");

    $("#upload_form").on("submit", function (e) {
      e.preventDefault();
    //   var form = $(this);
      var formData = new FormData(this);
      const media_data = input_file.files[0];
      if (media_data != null) {
        console.log(media_data);
        progress_bar.classList.remove("not-visible");
      }

      $.ajax({
        type: "POST",
        url: window.location.href,
        data: formData,
        dataType: "json",
        beforeSend: function () {
          $(".btn-save-contacts").attr("disabled", true);
          $(".btn-save-contacts").text("Please wait...");
        },
        complete: function () {
          $(".btn-save-contacts").attr("disabled", false);
          $(".btn-save-contacts").text("Upload Contacts");
        },
        xhr: function () {
          const xhr = new window.XMLHttpRequest();
          xhr.upload.addEventListener("progress", (e) => {
            if (e.lengthComputable) {
              const percentProgress = (e.loaded / e.total) * 100;
              progress_bar.innerHTML = `<div class="progress-bar progress-bar-striped bg-success" 
                    role="progressbar" style="width: ${percentProgress}%" aria-valuenow="${percentProgress}" aria-valuemin="0" 
                    aria-valuemax="100"></div>`;
            }
          });
          return xhr;
        },
        success: function (response) {
          uploadForm.reset();
          progress_bar.classList.add("not-visible");
            Swal.fire({
                title: "Upload Success",
                text: response.message,
                icon: "success",
                confirmButtonText: "Ok",
            });
        },
        error: function (err) {
            progress_bar.classList.add("not-visible");
            Swal.fire({
                title: "Upload Error",
                text: "An error occurred while uploading the contacts",
                icon: "error",
                confirmButtonText: "Ok",
              });
        },
        cache: false,
        contentType: false,
        processData: false,
      });
    });

    $(".form-smtp").on("submit", function (e) {
      e.preventDefault();
      const form = $(this);
      $.ajax({
        url: window.location.url,
        method: "POST",
        data: form.serialize(),
        type: "json",
        beforeSend: function () {
          $(".btn-save-smtp").attr("disabled", true);
          $(".btn-save-smtp").text("Please wait...");
        },
        complete: function () {
          $(".btn-save-smtp").attr("disabled", false);
          $(".btn-save-smtp").text("Save Settings");
        },
        success: function (res) {
          if (res.status) {
            Swal.fire({
              title: "Saving Success",
              text: res.message,
              icon: "success",
              confirmButtonText: "Ok",
            }).then(() => {
              window.location.href = "/smtp-list/";
            });
          } else {
            Swal.fire({
              title: "SMTP Error",
              text: res.message,
              icon: "error",
              confirmButtonText: "Ok",
            });
          }
        },
        error: function (err) {
          Swal.fire({
            title: "Server Error",
            text: "An error occurred while saving the smtp settings",
            icon: "error",
            confirmButtonText: "Ok",
          });
        },
      });
    });

    $(document).ready(function () {

      // Handle form submission
      $("#smtp-test-form").submit(function (e) {
        e.preventDefault();

        var form = $(this);
        var formData = form.serialize(); // Serialize the form data

        $.ajax({
          url: "/smtp-test/",
          type: "POST",
          data: formData,
          beforeSend: function () {
            $(".btn-test-smtp").attr("disabled", true);
            $(".btn-test-smtp").text("Testing...");
          },
          complete: function () {
            $(".btn-test-smtp").attr("disabled", false);
            $(".btn-test-smtp").text("Send Test Email");
          },
          success: function (response) {
            if (response.status) {
              $("#smtp-test-success").text(response.message).show();
              $("#smtp-test-primary").hide();
            } else {
              $("#smtp-test-error").text(response.message).show();
              $("#smtp-test-success").hide();
            }
          },
          error: function () {
            $("#smtp-test-primary")
              .text("An error occurred. Please try again.")
              .show();
            $("#smtp-test-success").hide();
          },
        });
      });
    });

    $(".form-campaigns").on("submit", function (e) {
      e.preventDefault();
      const form = $(this);
      $.ajax({
        url: window.location.url,
        method: "POST",
        data: form.serialize(),
        type: "json",
        beforeSend: function () {
          $(".btn-save-campaign").attr("disabled", true);
          $(".btn-save-campaign").text("Please wait...");
        },
        complete: function () {
          $(".btn-save-campaign").attr("disabled", false);
          $(".btn-save-campaign").text("Save Campaign");
        },
        success: function (res) {
          if (res.status) {
            Swal.fire({
              title: "Saving Success",
              text: res.message,
              icon: "success",
              confirmButtonText: "Ok",
            }).then(() => {
              window.location.href = "/campaigns/";
            });
          } else {
            Swal.fire({
              title: "Campaign Error",
              text: res.message,
              icon: "error",
              confirmButtonText: "Ok",
            });
          }
        },
        error: function (err) {
          Swal.fire({
            title: "Server Error",
            text: "An error occurred while saving the campaign",
            icon: "error",
            confirmButtonText: "Ok",
          });
        },
      });
    });

    $(".form-settings").on("submit", function (e) {
      e.preventDefault();
      const form = $(this);
      $.ajax({
        url: window.location.url,
        method: "POST",
        data: form.serialize(),
        type: "json",
        beforeSend: function () {
          $(".btn-save-settings").attr("disabled", true);
          $(".btn-save-settings").text("Please wait...");
        },
        complete: function () {
          $(".btn-save-settings").attr("disabled", false);
          $(".btn-save-settings").text("Save Settings");
        },
        success: function (res) {
          if (res.status) {
            Swal.fire({
              title: "Saving Success",
              text: res.message,
              icon: "success",
              confirmButtonText: "Ok",
            }).then(() => {
              window.location.reload();
            });
          } else {
            Swal.fire({
              title: "Settings Error",
              text: res.message,
              icon: "error",
              confirmButtonText: "Ok",
            });
          }
        },
        error: function (err) {
          Swal.fire({
            title: "Server Error",
            text: "An error occurred while saving the settings",
            icon: "error",
            confirmButtonText: "Ok",
          });
        },
      });
    });


    document.getElementById("actionSelect").addEventListener("change", function () {
    var selectedAction = this.value;
    if (selectedAction) {
        window.location.href = selectedAction;
    }
    });
})(jQuery);

