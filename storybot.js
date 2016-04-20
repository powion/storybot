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
                    "frodo was delighted with a wave of all that we make up good deal about them , and then we shall be able master , who are unused to find the world is changing now called accursed hills . but samwise , will you each each time , we can keep awake could make only for a guess at hand , and they felt the wind seemed in its choked path . he jumped up and went to out , wet sky . the grass , but in other the language of orthanc yet at last , to elvenhome that that he could deal with them . but who has studied heard something that would be a danger , as if thinking they had walked for the time comes of a great storm ship , wrought of living men were dead , so near that even the hobbits and strode forward , using the authority weapon . i will take neither strength of the elves , ? very mighty works of gondor that the company was arranged taking ."
                  ]
            },
            // TOLKIEN ---------------------------------------------------------
            {
                name:"Tolkien",
                hide:true,
                text:[
                  // tolkien text 1
                  "frodo was delighted with a wave of all that we make up good deal about them , and then we shall be able master , who are unused to find the world is changing now called accursed hills . but samwise , will you each each time , we can keep awake could make only for a guess at hand , and they felt the wind seemed in its choked path . he jumped up and went to out , wet sky . the grass , but in other the language of orthanc yet at last , to elvenhome that that he could deal with them . but who has studied heard something that would be a danger , as if thinking they had walked for the time comes of a great storm ship , wrought of living men were dead , so near that even the hobbits and strode forward , using the authority weapon . i will take neither strength of the elves , ? very mighty works of gondor that the company was arranged taking ."
                ]
            },
            // TIFU ------------------------------------------------------------
            {
                name:"Reddit: TIFU",
                hide:true,
                text:[
                  "today i fucked up , not you . i know better then then to come up from behind on someone who has seen seen what you have seen . i am so relieved . . beyond relieved . my boyfriend now knows that sexy time time is done . so he starts cleaning up our bedroom bedroom . i asked him to help me remove it so so we could continue . mother of god ... it smelled smelled like an eviscerated decomposing body mixed with rotting broccoli , , sewage , and rotting eggs all in one . and and the smell did not go away . i threw out out the cup and its contents , but the stench of of 14 day old rotting blood and uterine gunk is not not one that fades easily . i could tell my squeamish dad , but he would make me call my mom and and tell her everything.i am still on his account and going going to subscribe to every gay porn subreddit i can find find .",

                      "he opened his eyes and stood upright in the tub tub . its little brown head poking out and looking at at me in disappointment and fear . what was going to to happen . dan started looking around his sister 's room room . the alcohol intensified both of our libidos , so so we started making out and realized there was no obvious obvious place to continue but in the car itself . . . . so we did . i put the back seats seats down and we got to it . . . and and i 'm starting to put together in my mind , , and proudly proclaim , `` i fucked my horse ! ! '' . i rush downstairs into a kitchen billowing disgusting disgusting , black smoke , and see a skinny man , , crouched very low , scuttle around a parked car ."
                ]
            }
        ];

        $scope.currentSource = $scope.sources[0];
    });
} catch(e) {
    console.log(e);
}
