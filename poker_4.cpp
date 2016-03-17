#include <iostream>
#include <string>
#include <assert.h>
using namespace std;

const string str_suits[4] = {"clubs", "diamonds", "hearts", "spades"};
const string str_cards[13] = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"};

string printCard(int c)
{
	if (c > -1){return str_cards[c/4] + " of " + str_suits[c%4];}
	else {return "not a card";}
}

//finds the highest-ranked flush of suit k, provided one exists
void extractFlush(int* common_cards[5], int hand[2], int &k, int flush[5])
{
	int cards[7] = {-2,-2,-2,-2.-2,-2,-2};
	for(int i = 0;i < 5; i++)
	{
		cards[i] = ((*common_cards[i]%4 == k) ? *common_cards[i] : -1);
	}

	cards[5] = ((hand[0]%4 == k) ? hand[0] : -1);
	cards[6] = ((hand[1]%4 == k) ? hand[1] : -1);

	sort(cards, cards+7);
	//reverse(cards,cards+7);

	//for(int i = 0;i < 5; i++){flush[i] = cards[6-i];}
	for(int i = 0; i < 5; i++)
	{
		flush[i] = cards[6-i];
		if (flush[i] == -1)
		{
			//cout << *common_cards[0] << ", " << *common_cards[1] << ", " << *common_cards[2] << ", " << *common_cards[3] << ", " << 
			//*common_cards[4] << ", " << hand[0] << ", " << hand[1] <<  "    k = " << k << endl;
		}
	}
}

//finds the highest ranked straight flush of suit k, given one exists
void checkStraightFlush(int* common_cards[5], int hand[2], int straightflush[5], int k, bool print)
{
	int cards[7] = {-2,-2,-2,-2.-2,-2,-2};
	for(int i = 0;i < 5; i++)
	{
		cards[i] = ((*common_cards[i]%4 == k) ? *common_cards[i] : -1);
	}

	cards[5] = ((hand[0]%4 == k) ? hand[0] : -1);
	cards[6] = ((hand[1]%4 == k) ? hand[1] : -1);

	sort(cards, cards+7);

	if (print)
	{
		for(int i = 0; i < 7; i++)
		{
			cout << cards[i] << ' ' << endl;
		}
		cout << endl;

		for(int i = 0; i < 7; i++)
		{
			cout << cards[i]<< endl;
		}
		cout << endl;
	}
	
	int i = 6;
	int count = 0;
	int previous = cards[6] + 4;
	while((i > -1) && (cards[i] > -1))
	{
		if (cards[i] == previous - 4){count++;}
		else {count = 1;}

		previous = cards[i];

		if (print){cout << count << endl;}

		if (count > 4)
		{
			for(int j = 0; j < 5; j++)
			{
				straightflush[j] = cards[i+j];
			}
		break;
		}
		i--;
	}

	reverse(straightflush, straightflush+5);
}

//checks for 4-of-a-kind, triples, and pair:
inline void checkTuples(int cards_table[], int four_of_a_kind[], int three_of_a_kind[], int twopair[], int pair[])
{
	for(int k = 12; k > -1; k--)
	{
		if (cards_table[k] == 4)
		{
			//cout << d[i] << ' ' << d[j] << endl;
			four_of_a_kind[0] = k;
		}

		else if ((cards_table[k] == 3) && (three_of_a_kind[0] == -1))
		{
			three_of_a_kind[0] = k;
		}

		else if (cards_table[k] == 2)
		{
			if (pair[0] == -1)
			{
				pair[0] = k;
			}
			else if (twopair[0] == -1)
			{
				twopair[0] = pair[0];
				twopair[1] = k;
			}
		}
	}
}

//puts common (table) cards into piles based on rank, suit
void sortTableCards(int* common_cards[5], int cards_table[13], int suits_table[4])
{
	fill(cards_table,cards_table+13, 0);
	fill(suits_table,suits_table+4, 0);
	
	for(int i = 0; i < 5; i++)
	{	
		cards_table[*common_cards[i]/4]++;
		suits_table[*common_cards[i]%4]++;
	}
}

//checks for flush
inline void checkFlush(int* common_cards[5], int hand[2], int suits_table[4], int flush[5])
{
	int flush_tmp = -1;
	for(int k = 0; k < 4; k++)
	{
		if (suits_table[k] > 4)
		{
			flush_tmp = k;
			break;
		}
	}
	if (flush_tmp != -1)
	{
		extractFlush(common_cards, hand, flush_tmp, flush);
	}
}

//checks for straight
inline void checkStraight(int cards_table[13], int straight[])
{
	int c = 0;
	for(int k = 0; k < 13; k++)
	{
		if (cards_table[k] > 0) {c++;}
		else {c = 0;}

		if (c > 4) 
		{	
			//cout << "Straight: " << printCard(d[i]) << ", " << printCard(d[j]) << endl;
			straight[0] = k;
			break;
		}
	}
}

//checks for fullhouse
inline void checkFullHouse(int fullhouse[2], int three_of_a_kind[2], int pair[2])
{
	if ((pair[0] != -1) && (three_of_a_kind[0] != -1))
	{
		fullhouse[0] = three_of_a_kind[0];
		fullhouse[1] = pair[0];
	}
}

//checks all the combinations which a given set of cards satisfies
void comboCheck(int* common_cards[5], int cards_table[13], int suits_table[4], int hand[2], int* combos[8])
{
	/*
	int straightflush[5] = combos[0];
	int four_of_a_kind[1] = combos[1];
	int fullhouse[2] = combos[2];
	int flush[5] = combos[3];
	int straight[1] = combos[4];
	int three_of_a_kind[1] = combos[5];
	int twopair[2] = combos[6];
	int pair[2] = combos[7];
	*/

	//temporarily adding the cards in the player's hand to the "table"
	cards_table[hand[0]/4] += 1;
	cards_table[hand[1]/4] += 1;

	suits_table[hand[0]%4] += 1;
	suits_table[hand[1]%4] += 1;

	checkTuples(cards_table, combos[1], combos[5], combos[6], combos[7]);
	checkFullHouse(combos[2], combos[5], combos[7]);
	checkFlush(common_cards, hand, suits_table, combos[3]);
	checkStraight(cards_table, combos[4]);

	if ((combos[4][0] != -1) && (combos[3][0] != -1))
	{
		checkStraightFlush(common_cards, hand, combos[0], combos[3][0]%4, 0);// ((d[i] == 1) && (d[j] == 40)));
	}

	//removing cards in player's hand from the "table"
	cards_table[hand[0]/4] -= 1;
	cards_table[hand[1]/4] -= 1;

	suits_table[hand[0]%4] -= 1;
	suits_table[hand[0]%4] -= 1;
}

//given combos, updates highest_combo and combo_counters (if applicable)
inline void updateCounters(int* combos[7], int &highest_combo, int combo_counters[8])
{
	for(int k = 0; k < 8; k++)
	{
		if (combos[k][0] != -1)
		{
			if (combo_counters) {combo_counters[k]++;}
			highest_combo = k;
			break;
		}
	}	
}

//resolves a tie
int tieBreak(int* common_cards[8], int cards_table[13], int suits_table[4], 
			int player_hand[2], int op_hand[2], int player_combo[], int op_combo[], int highest_combo)
{
	return 1; 
}

float computeHandStrength(int op_hands[47][47][2])
{
	int wins = 0;
	int ties = 0;

	for(int i = 0; i < 47; i++)
	{
		for(int j = i+1; j < 47; j++)
		{
			wins += op_hands[i][j][0];
			ties += op_hands[i][j][1];
		}
	}

	return 1. - (float(wins) + 0.5*float(ties))/1070190;
}

int main()
{
	int flop[3] = {38,34,50};
	int hand[2] = {6,1};

	cout << endl << "hand:" << endl;
	for(int i = 0; i < 2; i++)
	{
		cout << str_cards[hand[i]/4] + " of " + str_suits[hand[i]%4] << endl;
	}

	cout << endl << "flop:" << endl;
	for(int i = 0; i < 3; i++)
	{
		cout << str_cards[flop[i]/4] + " of " + str_suits[flop[i]%4] << endl;
	}
	cout << endl;

	//computing how many cards of each suit appear in the flop, hand
	int suits_flop[4] = {0,0,0,0};
	int suits_hand[4] = {0,0,0,0};
	for(int i = 0; i < 3; i++)
	{
		suits_flop[flop[i]%4]+= 1;
		if(i<2)
		{
			suits_hand[hand[i]%4] += 1;
		}
	}

	//computing how many cards of each value appear in the flop, hand
	int cards_flop[13] = {0,0,0,0,0,0,0,0,0,0,0,0,0};
	int cards_hand[13] = {0,0,0,0,0,0,0,0,0,0,0,0,0};
	for(int i = 0; i < 3; i++)
	{
		cards_flop[flop[i]/4]+= 1;
		if(i<2)
		{
			cards_hand[hand[i]/4] += 1;
		}
	}

	//intialization of d, an array containing all the cards not in the flop & hand.
	int d[47];
	int a = 0;
	for(int i = 0; i < 52; i++)
	{
		if ((flop[0] == i) || (flop[1] == i) || (flop[2] == i) || (hand[0] == i) || (hand[1] == i))
		{
			a++;
			//cout << i << ' ' << a << endl;
		}

		else {d[i-a] = i;}
	}
	
	//initializing op_hands, the array of possible opponent hands symmetric and thus half-filled (upper triangular)
	//For each hand, it will count how many times out of (45 choose 2) that hand will win [0], and how many times it will tie [1]
	int op_hands[47][47][2];
	for(int i = 0; i <47; i++)
	{
		for(int j = 0; j < 47; j++)
		{
			op_hands[i][j][0] = 0;
			op_hands[i][j][1] = 0;
		}
	}

	//these are -1 if given combo does not appear, and otherwise serve to identify the combo
	int four_of_a_kind[1] = {-1};
	int three_of_a_kind[1] = {-1};
	int pair[1] = {-1};
	int twopair[2] = {-1,-1};
	int fullhouse[2] = {-1,-1};
	int flush[5] = {-1,-1,-1,-1,-1};
	int straight[1] = {-1};
	int straightflush[5] = {-1,-1,-1,-1,-1};

	int *combos[8] = {straightflush, four_of_a_kind, fullhouse, flush, straight, three_of_a_kind, twopair, pair};
	int combo_counters[8] = {0,0,0,0,0,0,0,0};

	//declaration of d2, an array which will contain all the cards in d, 
	//excluding the additional two on the table
	int d2[45];

	int *common_cards[5] = {&flop[0], &flop[1], &flop[2], NULL, NULL};

	int tieCounter = 0;

	//first main loop, over the 2 remaining table cards
	for(int i = 0; i < 47; i++)
	{
		for(int j = i+1; j < 47; j++)
		{
			//adding the newly generated table cards to common_cards
			common_cards[3] = &d[i];
			common_cards[4] = &d[j];

			//resetting all the player combos
			for(int k = 0; k < 8; k++)
			{
				combos[k][0] = -1;
			}

			//generting cards_table and suits_table, which keep track of how many cards of each rank and suit lie on the table 
			int cards_table[13];
			int suits_table[4];
			sortTableCards(common_cards, cards_table, suits_table);

			//checking for combos
			comboCheck(common_cards, cards_table, suits_table, hand, combos);

			//initialization of d2
			int b = 0;
			for(int k = 0; k < 47; k++)
			{
				if ((i == d[k]) || (j == d[k])){b++;}
				else {d2[k-b] = k;}
			}

			int highest_combo = -1; //the highest combination acheived by player

			//updating combo counters and highest_combo
			updateCounters(combos, highest_combo, combo_counters);

			int win; //will keep track of whether a given prospective opponent hand wins over player's hand. 
					 //-1 if the hand loses, 1 if it wins, 0 if it ties and some more work needs to be done.

			//initializing all the opponent combos to false
			int op_four_of_a_kind[1] = {-1};
			int op_three_of_a_kind[1] = {-1};
			int op_pair[1] = {-1};
			int op_twopair[2] = {-1,-1};
			int op_fullhouse[2] = {-1,-1};
			int op_flush[5] = {-1,-1,-1,-1,-1};
			int op_straight[1] = {-1};
			int op_straightflush[5] = {-1,-1,-1,-1,-1};

			int* op_combos[8] = {op_straightflush, op_four_of_a_kind, op_fullhouse, op_flush, 
									  op_straight, op_three_of_a_kind, op_twopair, op_pair};

			int op_hand[2] = {-1,-1};
			int op_highest_combo = -1;

			//second loop, over possible opponent hands
			for(int k = 0; k < 45; k++)
			{
				for(int l = k+1; l < 45; l++)
				{
					op_hand[0] = d[d2[k]];
					op_hand[1] = d[d2[l]];
					comboCheck(common_cards, cards_table, suits_table, op_hand, op_combos);

					updateCounters(op_combos, op_highest_combo, NULL);

					if (op_highest_combo > highest_combo) //opponent wins
					{
						op_hands[d2[k]][d2[l]][0]++;
					}
					else if (op_highest_combo == highest_combo) //undetermined, needs a tie break
					{
						op_hands[d2[k]][d2[l]][1] += tieBreak(common_cards, cards_table, suits_table, hand, op_hand,
													combos[highest_combo], op_combos[highest_combo], highest_combo);
						tieCounter++;
					}
				}
			}
		}
	}

	float hand_strength = computeHandStrength(op_hands);

	cout << "straight flush: " << combo_counters[0] << endl;
	cout << "four of a kind: " << combo_counters[1] << endl;
	cout << "full house: " << combo_counters[2] << endl;
	cout << "flush: " << combo_counters[3] << endl;
	cout << "straight: " << combo_counters[4] << endl;
	cout << "three of a kind: " << combo_counters[5] << endl;
	cout << "two pair: " << combo_counters[6] << endl;
	cout << "pair: " << combo_counters[7] << endl << endl;
	cout << "tieCounter: " << tieCounter << endl;
	cout << "hand strength: " << hand_strength << endl << endl;
  return 0;
}