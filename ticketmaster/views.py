from django.shortcuts import render, redirect
import requests
import math
import datetime
# from .Forms import CommentForm
from django.http import JsonResponse
from .models import Comments


# Create your views here.
def ticketmaster_api(term, city):
    try:
        url = "https://app.ticketmaster.com/discovery/v2/events"
        params = {
            "ClassificationName": term,
            "city": city,
            "sort": 'date,asc',
            "apikey": '6zwPWGcRG3kYonWok7xRtL8tldSzKB5y'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        results = response.json()
        return results
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def search(request):
    search_alert = False
    city_alert = False
    no_results = False
    display = False

    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        city = request.POST.get('city')
        if search_term == "":
            search_alert = True
        elif city == "":
            city_alert = True
        if search_alert is False and city_alert is False:
            display = True
            search_info = ticketmaster_api(search_term, city)
            event_total = search_info["page"]["totalElements"]
            if event_total == 0:
                no_results = True
            else:
                events = search_info["_embedded"]["events"]
                event_num = len(events)
                event_name = []
                event_id = []
                image_num = []
                event_image = []
                event_start = []
                venue = []
                venue_name = []
                city_name = []
                state = []
                address = []
                url = []
                no_specific_time = []
                time_tba = []
                date = []
                time = []
                event_info = None
                comments_list = []
                for i in range(event_num):
                    event = events[i]
                    event_name.append(event["name"])
                    event_id.append(event["id"])
                    image_num.append(len(event["images"]))
                    event_image.append(event["images"][math.floor(((image_num[i] - 1) / 2))]["url"])
                    event_start.append(event["dates"]["start"])
                    venue.append(event["_embedded"]["venues"][0])
                    venue_name.append(venue[i]["name"])
                    city_name.append(venue[i]["city"]["name"])
                    state.append(venue[i]["state"]["name"])
                    address.append(venue[i]["address"]["line1"])
                    url.append(event["url"])

                    event_id2 = event["id"]
                    print(event_id2)

                    comments = Comments.objects.filter(event_id__contains=f"{event_id2}")
                    comments_list.append(comments)

                    for comment in comments:
                        print('comment:', comment.comment)

                    # display time
                    no_specific_time.append(event_start[i]["noSpecificTime"])
                    time_tba.append(event_start[i]["timeTBA"])
                    date.append("")
                    time.append("")
                    if no_specific_time[i] is False and time_tba[i] is False:
                        raw_date = event_start[i]["dateTime"]
                        date[i] = datetime.datetime.strptime(raw_date,
                                                             '%Y-%m-%dT%H:%M:%S%fZ').strftime("%a %b %d %Y")
                        local_time = "" + event_start[i]["localTime"]
                        time_vals = local_time.split(':')
                        if int(time_vals[0]) > 12:
                            time[i] = str(int(time_vals[0]) - 12) + ':' + time_vals[1] + ' PM'
                        else:
                            time[i] = str(int(time_vals[0])) + ':' + time_vals[1] + ' AM'
                    else:
                        date[i] = "No Date"
                    event_info = zip(event_name, event_image, time, venue_name, city_name, state, address, url, date,
                                     event_id, comments_list)

                # print(comments)

                context = {'search_alert': search_alert, 'city_alert': city_alert, 'no_results': no_results,
                           'display': display, 'event_num': event_num, 'event_info': event_info}
                return render(request, 'ticketmaster.html', context)

    context = {'search_alert': search_alert, 'city_alert': city_alert, 'no_results': no_results, 'display': display}
    return render(request, 'ticketmaster.html', context)


#    def comments(request):
# def create_comments(request):
#     # Create a form instance and populate it with data from the request
#     form = CommentForm(request.POST or None)
#     # check whether it's valid:
#     if form.is_valid():
#         # save the record into the db
#         form.save()
#         # after saving redirect to view_product page
#         return redirect('search')
#
#     # if the request does not have post data, a blank form will be rendered
#     return None


def add_comment(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        comment = request.POST.get('comment')
        print(event_id + '  ' + comment)
        Comments.objects.create(comment=comment, event_id=event_id)
        return JsonResponse(

            {
                'added': True,
                'message': 'Success'
            }
        )
    else:
        return JsonResponse(

            {'message': 'Something went wrong'}
        )


def delete_comment(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        if event_id is not None:
            comment = Comments.objects.get(id=event_id)
            comment.delete()
            return JsonResponse(
                {
                    'removed': True,
                    'message': 'Success'
                }
            )
    else:
        return JsonResponse(

            {'message': 'Something went wrong'}
        )

