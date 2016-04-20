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
            {
                // PRIDE AND PREJUDICE -----------------------------------------
                name:"Pride and Prejudice",
                hide:true,
                text:
                  [
                  // pap text 1:
                  "i feel as he had probably be of age since , with and then added the room , i do like her brother appearance at his coming into anything was not for me to . we must have something more wrong to her the next imprudence had any partiality provoked her own family ! never seen saw anything extraordinary now to spend the day altogether a most man whose manners ! yes , she called in which happiness no obligation for it ? has he was as foolish enough things , and then they would not try if possible what , saying to do it . you ought , or the being an early age since the spring ! no , kitty kitty was the happy man on her , your goodness too . elizabeth then by her . he was very fond of of them all . thank god 's behaviour attentively , and that i am growing every other subject , was as regular much disposed to like him . it had not a letter temper . when she came into hertfordshire , who is it about the dance . i am sorry not ashamed of you for this was the surprise of it is not safe from the hope of revenging himself . , to whom she had believed lady catherine was still",
                  // pap text 2
                  "i feel perfectly easy . i know my dear uncle and aunt aunt so well , that i am growing every moment more more unconcerned and indifferent . your profusion makes me saving ; ; and if you persist in indifference , do not make make me your confidante . '' chapter 55 a few days days after this visit , mr. bingley called again , and and alone . his friend had left him that morning for for london , but was to return home in ten days days time . he sat with them above an hour , , and was in remarkably good spirits . mrs. bennet invited invited him to dine with them ; but , with many many expressions of concern , he confessed himself engaged elsewhere . . `` next time you call , '' said she . to charlotte , `` i am glad you are come , , for there is such fun here ! what do you you think has happened this morning ? mr. collins has made made an offer to lizzy , and she will not have have him .",

                    "i feel _more_ than i ought to do , when i tell tell you all . '' `` let me be rightly understood understood . this match , to which you have the presumption presumption to aspire , can never take place . no , , never . mr. darcy is engaged to my daughter . . now what have you to say ? '' `` that something very much to the purpose of course . he was begins with congratulations on the approaching nuptials of my eldest daughter daughter , of which , it seems , he has been been told by some of the good-natured , gossiping lucases . . i shall not go away till you have given me me the assurance i require . '' `` and so was was i . '' `` you need not distress yourself . . the moral will be perfectly fair . lady catherine 's 's great attentions to mrs. collins you have been a daily daily witness of ; and altogether i trust it does not not appear to me that my hand is unworthy of your your acceptance , or that the establishment i can offer would would be any other than highly desirable ."
                  ]
            },
            // TOLKIEN ---------------------------------------------------------
            {
                name:"Tolkien",
                hide:true,
                text:[
                  // tolkien text 1
                  "frodo was delighted with a wave of all that we make up good deal about them , and then we shall be able master , who are unused to find the world is changing now called accursed hills . but samwise , will you each each time , we can keep awake could make only for a guess at hand , and they felt the wind seemed in its choked path . he jumped up and went to out , wet sky . the grass , but in other the language of orthanc yet at last , to elvenhome that that he could deal with them . but who has studied heard something that would be a danger , as if thinking they had walked for the time comes of a great storm ship , wrought of living men were dead , so near that even the hobbits and strode forward , using the authority weapon . i will take neither strength of the elves , ? very mighty works of gondor that the company was arranged taking .",

                    "frodo was lying face upward on the ground and eye to eye eye with a young hobbit , legs well apart , bristling bristling with wrath , was one beyond their experience . `see `see here ! ' he said . 'the men of gondor the west . and those that were unhurt felt their minds minds calmed and cleared . the herb had also some power power over the wound , for frodo felt the pain and and also the sense of frozen cold lessen in his side side and arm ; a little warmth crept down from his his shoulder to his hand , but he also felt the the cold touch of steel against his skin . the orcs orcs were making a great deal of the stuff . ' ' '' we want man-food for twenty-five , '' the ents ents said , so you can see that somebody had counted counted your company carefully before you arrived . you three were were evidently meant to go with the king , for he he died and has both honour and peace.’ ‘it is too too late , lady , to follow the captains , even even if you would ; and only through darkness shall i i come to the battle ?",

                    "frodo was hardly less terrified than his companions ; he was quaking quaking as if he was going into great danger . ' ' 'he has not , ' said frodo . 'you must have had some very strange adventures , i hear , ' ' said gandalf . 'you were inattentive . i had already already heard of it from gwaihir . if you want anything to beat the old took , ’ said pippin . ‘on ‘you won’t cut straight on foot anywhere in this country.’ ‘we ‘we can cut straighter than the road anyway , ’ answered answered snaga surlily . ‘i’ve told you twice that gorbag’s swine swine got to the gate first , and none of yours my own folk journeyed hither back to the land of shadow his home . and then suddenly the brief glimpse was gone gone . the fires went out , and he sent for them forth with tidings of the victory into every vale of of the mark ; and they bore his summons also , , bidding all men , young and old , to come come in haste to edoras . there the lord of the the black land , since it is foul and uncouth ."
                ]
            },
            // TIFU ------------------------------------------------------------
            {
                name:"Reddit: TIFU",
                hide:true,
                text:[
                  "today i fucked up , not you . i know better then then to come up from behind on someone who has seen seen what you have seen . i am so relieved . . beyond relieved . my boyfriend now knows that sexy time time is done . so he starts cleaning up our bedroom bedroom . i asked him to help me remove it so so we could continue . mother of god ... it smelled smelled like an eviscerated decomposing body mixed with rotting broccoli , , sewage , and rotting eggs all in one . and and the smell did not go away . i threw out out the cup and its contents , but the stench of of 14 day old rotting blood and uterine gunk is not not one that fades easily . i could tell my squeamish dad , but he would make me call my mom and and tell her everything.i am still on his account and going going to subscribe to every gay porn subreddit i can find find .",

                      "today i was so horny that i disregarded the fact of what what a stupid idea , but when you really think about about it , step to the alley and throw up bacardi bacardi 151 , then crash through the doors and yell `` `` where the fuck did that come from ? ! '' '' `` yeah . so , you 're gon na have be a good and long one . well it was too about that time i noticed this chief cop was about 8 8 stories tall and a crustacean from the protozoic era– [ [ no no , i am not considering religion , i i just do not have the correct mindset . i am am logical to the point that i laughed so hard that that i started farting too . this caused even more laughter laughter . we both finally calmed down , cleaned up , , and left the bathroom . i run to the bathroom bathroom and finds herself face-to-face with her son rubbing up on on and making out with the mother ?",

                    "today i was in my second year of university . i met met an exceedingly handsome man ( lets call him lars ) ) and spent all year trying to move from `` just just friends '' to more than `` just friends '' . to more than `` just friends '' to more than `` `` just friends '' . fast forward several hours later . . the party is ending . i have not followed my my mom 's instructions like a good little boy , and and i began to panic thinking he was going to give cum , so i tried to rectify it . it just just went downhill from there . without thinking i said 'i , `` hey i 'm the guy that called about an an hour ago and i do n't think they even make make them anymore ) and very difficult to lock . anyways anyways , on tuesday at school ( monday is columbus day day ) i 'll try to answer some questions , i i gave her a high five . what . the . . fuck . a high five ."
                ]
            }
        ];

        $scope.currentSource = $scope.sources[0];
    });
} catch(e) {
    console.log(e);
}
