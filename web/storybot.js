try {
    var app = angular.module('myApp', []);

    app.controller('myCtrl', function($scope) {

        // Change stories based on source selected
        // Called when tab items are clicked
        $scope.selectSource = function ($event, $source) {
            $scope.currentSource.hide = true;
            $scope.currentSource = $source;
            $scope.currentSource.hide = false;
            // highligt the currently selected tab
            tabitems = document.getElementsByClassName("tabitems");
            for (i = 0; i < tabitems.length; i++) {
                tabitems[i].className = tabitems[i].className
                    .replace(" w3-dark-grey", "");
            }
            $event.currentTarget.className += " w3-dark-grey";
            $scope.selectText(0);
        };

        $scope.currentTextIndex = 0;
        $scope.selectNextText = function () {
            $scope.currentTextIndex += 1;
            $scope.selectText($scope.currentTextIndex);
        }

        $scope.selectPrevText = function () {
            $scope.currentTextIndex -= 1;
            $scope.selectText($scope.currentTextIndex);
        }

        // Select a specific text from the current source
        $scope.selectText = function ($index) {
            texts = document.getElementsByClassName(
                $scope.currentSource.name + "-texts"
            );

            if ($index >= texts.length) {
                $index = 0;
            } else if ($index < 0) {
                $index = texts.length - 1;
            }

            for (i = 0; i < texts.length; i++) {
                texts[i].style.display = "none";
            }

            texts[$index].style.display = "block";
            $scope.currentTextIndex = $index;
        };

        $scope.sources = [
            // TIFU ------------------------------------------------------------
            {
                name:"TIFU",
                hide:true,
                text:[
                  "After a moment he ran out of the bathroom and started screaming in the lobby. The seat was up so i tried to take a quick deep breath so i could n't imagine what else it could be fixed. She tells me she is done dating. I do n't think i 've ever cried with laughter. I find the guy fawkes skeleton conversation on the floor of the deck and watch something. I said no she 's way out of my league she said then how are you dating me and tells me it is time to wait. Me being the mean. She tried to get to the porch and i are still together. We are trying to fix things our way back from school to an empty house so i decided. A few people started watching me and the security guard that she had an assignment. ",

                      "Today i 'll pull over and give him the correct bag and explain i meant to say was would you prefer to work on my break this morning and my roommate made a new home. I wish i never started it. The absolute second i finish my sentence the word. After a moment he ran out of the office the effect of the one-way surgical. In one night i got drunk and started pushing her around and i not paying attention to my footing flags. Then they called us over from the gas station we swung. It was kinda like that but no matter. I told them to wait until they finish their speech and get to bed. On my first day because we sometimes crush on the same girls. I am a guy not a girl. ",

                    "Today i was in my late teens teachers were not amused at his response : i 'm a programmer ship. And that is how i fucked up today. I really hope that you all will understand. I wo. So i went back to my house as we 're driving i mention to him i 'm thinkin mom and i 'm not interested in looking around the office because it is similar to. We know each other and i have no idea i 'm not a success either my sister or me. She 's 45 minutes ago and i may be in the passenger seat. I did n't know whether to laugh or to cry. I tried to forget. I step into my father 's right. ",

                    "Today i 'm walking into the grocery prank my stepdad. It 's become a point of contention. So i decided to tell my whole family the story. This will be a walk in the park compared attention. Tl dr : asked a guy to show me this in a comment on askreddit but i think it was 2 years accidental first guy i have her all wound up i slip off her dress. My dad works in the city and has a key to the apartment. I say no no just tell my mother. In the end i settled. Rip inbox : thanks anonymous. This was not surprising logged. "
                ]
            },
            // tales from retail ------------------------------------------------------------
            {
                name:"Tales From Retail",
                hide:true,
                text:[
                  "Today i had a guy think. I 'm a decorator. Finally she says that her grandson is 9 in total for one person to let her see the cop. Again we are closed. We 've spent over an hour with her at this point and we had never had a problem with that. In fact the reason she did n't do anything it just sat there. He gives me a short and rude no. Okay. I still input. A rational closer treatment routine. ",

                  "**me** : let me talk to your manager. You have terrible customer service skills. Keep in mind this girl is tiny. The ax x can meet your job. Me : i 'm sorry but since. He would whistle. Turns out she knows my mum small town and even things that my wife should do or usually offer but it 's not that hard. He went down. She 's looking to pick up some good stuff. We have a metal stand that goes in the hallway that holds our menu and more angry. ",

                  "Me : ... looking. The mom is dying of laughter. He never came back saying he did but the call was n't picked up. I tell her no unfortunately its against the rules. This woman had the patience of a different color. She expected that we would associate her 16 year old with her - and he turns away. I return with the box and after giving it a once over he buys a lot of stuff. I get there at 7:05. The kid went home. I asked my manager about it and learned the story : i 'm here but this happened yesterday and i felt like a million bucks. ",
                ]
            },
            {
                name:"Tales From Tech support",
                hide:true,
                text:[
                    "Please leave and get on the network. I come in one morning and 7 people were around the office. I couldn’t see the ghost in the computer room to fix my computer needs that. I mumbled to myself as i collected all my belongings maybe it would all work out. Soon after we noticed he started sometimes coming in on days he was n't scheduled to work and i have him email me the logs and i 'll be right down to help him. If he had n't been so lazy. They handle all alerts 3 : no it is sev. Me : can you send me a screenshot of the error occurred. It started out as a typical day i started i found out from some co-workers that the branch was known. He also had the next day off but what could the harm be.",

                        "Me : no. The conversation got ta go. Now type in : it allows me to script mouse. Last week 's notice that another drive was being encrypted on top of the box was an ibm. Me : what the hell is this. He was a little shocked i was willing. I pressed the wrong option on the phone because i ca cnc document standard. That seemed to get things sorted itself is usually a high-end. We 're distracted appropriately. Thanks again for that. ",

                        "Never heard of such a thing. What person needs $ 1200 of credit the only catch was getting business cards from his house. I went out and got another job and just decided to cut the coax. And was told that the only port for this on his laptop. I think back to the last couple of times i was holding. I got up from my chair staring at me. The user made an excuse. I tried to think of it. I 've never used that. The head builder started smiling. "
                ]
            },
            {
                name:"Petty Revenge",
                hide:true,
                text:[
                    "Edit : here 's a picture of a woman having a bad day or whatever. Super petty revenge. Whenever the smokers would go on their cigarette breaks we would stop working the rest of the stuff. My daughter was collecting figure it out. She has some galaxy returning jess was also planning on giving it to the manager anyway. He spends interior. I pointed to the man in the head and the last straw was when she called me at home and started swearing at me. She called me a stupid bitch a few times until one day she screamed at my younger sister. Her seat was empty besides mine. This taxi completely full of groceries from all walks of her coming in to write said note and so on the day she was down and depressed sticks. ",

                    "The police there 's a bunch. Since it was the best. He has long had a horrid very easy right next to me. I had seen the whole incident walked over and explained that he set them up and they are interrupting screaming. No. Well i do not want free samples given to the 3 apprentices. Ok i can do that. Except when i went into an empty gift card. The mc sends him to tell her to get a bit red in the face and says. Ok ... i 'll do my best to help them. ",

                    "Normally a pretty immature kiosk. Until i heard why is she likes to be clean it 's my car i say yes yes that sounds like a hell of a good idea to bring any kids at all. However i told them what you do and how many times. When the dad came up to the desk when the number. You did. The next morning he leaves and i go about my day the initial incident took place i was the acting supervisor who reports. He returns around 6:30 meanwhile the line. The right car decided he did n't want me to park in that spot. The guy behind me in line said they only have the two xbox 's left for lunch a couple times. I pick it up and plan to throw it on her doorstep. "
                ]
            },
            {
                name:"Pro Revenge",
                hide:true,
                text:[
                    "Well this guy and his brothers had had enough of him. The next week we were going to put them into school the next morning and got one with several replacement. I was walking down the hall and heard a large group of people and turns out melon decided to have a talk about john so i decided to go through this shit again i will set you on fire. No we did n't even work that night and i always id people. Do n't they ever figured it was just. So i ate all of the box. It 's about how i put a lot of money on tuition and i remember in my first meeting. Finally feeling tired lump and him and him douchebro turned red and walked out and we never saw him again either. I like to think that i was the one who the singer was with. She 's an english professor who had a very shallow law.",

                    "And now it is n't exactly relevant. I had to choose a rumour printed right next to the barracks room by room dumping the contents of everyone 's lockers to put our sketchbooks. She sent a picture of the ad he had to do to get the people involved. I contacted all the local news agencies to see who would do a block the # ... i 've always been straight in the eye and said i do n't really want to say that i am a member of a close friend. This friend who i 'll call lovely. Lovely. Lovely was a year ago. He 's big and dumb. They 've been together for over a year so i took my sweet ass time with getting back she was hungover. Fuck that.",

                    "I am not helping you. Just as we get him all settled in court. My dad turns around and finally confesses such a perfect. A replacement card cost 40 $ 800. I stop myself. 'do af want to get caught. So. The beginning of june we started moving on to say that rather than outside pissing on his arm. The stupid pencil is lost. This was devastating as it began to show."
                ]
            }
        ];

        $scope.currentSource = $scope.sources[0];
    });
} catch(e) {
    console.log(e);
}
