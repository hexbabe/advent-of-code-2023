// --- Day 7: Camel Cards ---
// Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship.
// (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends
// back to Island Island.

// "Did you bring the parts?"

// You turn around to see an Elf completely covered in white clothing, wearing goggles, and
// riding a large camel.

// "Did you bring the parts?" she asks again, louder this time. You aren't sure what parts
// she's looking for; you're here to figure out why the sand stopped.

// "The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

// After riding a bit across the sands of Desert Island, you can see what look like very large
// rocks covering half of the horizon. The Elf explains that the rocks are all along the part of
// Desert Island that is directly above Island Island, making it hard to even get there. Normally,
// they use big machines to move the rocks and filter the sand, but the machines have broken down
// because Desert Island recently stopped receiving the parts they need to fix the machines.

// You've already assumed it'll be your job to figure out why the parts stopped when she asks if
// you can help. You agree automatically.

// Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel
// Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

// In Camel Cards, you get a list of hands, and your goal is to order them based on the strength
// of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3,
// or 2. The relative strength of each card follows this order, where A is the highest and 2 is
// the lowest.

// Every hand is exactly one type. From strongest to weakest, they are:

// Five of a kind, where all five cards have the same label: AAAAA
// Four of a kind, where four cards have the same label and one card has a different label: AA8AA
// Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
// Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
// Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
// One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
// High card, where all cards' labels are distinct: 23456
// Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

// If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand.
// If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each
// hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand
// with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

// So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly,
// 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have
// the same first and second card).

// To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

// 32T3K 765
// T55J5 684
// KK677 28
// KTJJT 220
// QQQJA 483
// This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied
// by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand.
// Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

// So, the first step is to put the hands in order of strength:

// 32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.

// KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger
// (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.

// T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.

// Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with
// its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

// Find the rank of every hand in your set. What are the total winnings?

// --- Part Two ---
// To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards
// that can act like whatever card would make the hand the strongest type possible.

// To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order:
// A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

// J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered
// four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not
// the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

// Now, the above example goes very differently:

// 32T3K 765
// T55J5 684
// KK677 28
// KTJJT 220
// QQQJA 483
// 32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
// KK677 is now the only two pair, making it the second-weakest hand.
// T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
// With the new joker rule, the total winnings in this example are 5905.

// Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)


var (
	CARD_TO_VALUE = map[string]int{
		"A": 12,
		"K": 11, 
		"Q": 10, 
		"J": 9, 
		"T": 8, 
		"9": 7, 
		"8": 6, 
		"7": 5, 
		"6": 4, 
		"5": 3, 
		"4": 2, 
		"3": 1, 
		"2": 0,
	}

	CARD_TO_VALUE_JOKER = map[string]int{
		"A": 12,
		"K": 11, 
		"Q": 10, 
		"T": 9, 
		"9": 8, 
		"8": 7, 
		"7": 6, 
		"6": 5, 
		"5": 4, 
		"4": 3, 
		"3": 2, 
		"2": 1,
		"J": 0,
		"": -1,
	}
)

type Hand struct {
	cards       string
	bid         int
	cardToCount map[string]int
	value       int
}

func NewHand(cards string, bid int, usingJokerRule bool) Hand {
	hand := Hand{cards, bid, nil, -1}
	hand.cardToCount = hand.getCardToCount(usingJokerRule)
	hand.value = hand.GetValue()
	return hand
}

// returns the new cardToCount based on where to allocate the joker
func (hand Hand) applyJokerRule(usingJokerRule bool, cardToCount map[string]int) map[string]int {
	hand.cardToCount = cardToCount
	if !usingJokerRule || cardToCount["J"] == 0 {
		return cardToCount
	}

	if hand.isFiveOfAKind() {
		cardToCount["A"] = 5
		delete(cardToCount, "J")
		return cardToCount
	}
	
	if hand.isFourOfAKind() || hand.isFullHouse() {
		var otherCard string
		for card, _ := range cardToCount {
			if card != "J" {
				otherCard = card
				break
			}
		}
		cardToCount[otherCard] = 5
		delete(cardToCount, "J")
		return cardToCount
	}

	if hand.isThreeOfAKind() {
		if cardToCount["J"] == 3 {  // J is triplet, so change to best non-three
			bestCard := "J"
			for card, _ := range cardToCount {
				if CARD_TO_VALUE_JOKER[card] >= CARD_TO_VALUE_JOKER[bestCard] {
					bestCard = card
				}
			}
			cardToCount[bestCard] = 4
			delete(cardToCount, "J")
			return cardToCount
		} else {  // J is one of the single cards, so change to the triplet
			var tripletCard string
			for card, count := range cardToCount {
				if count == 3 {
					tripletCard = card
				}
			}
			cardToCount[tripletCard] = 4
			delete(cardToCount, "J")
			return cardToCount
		}
	}

	if hand.isTwoPair() {
		if cardToCount["J"] == 2 {  // J is one of the pairs
			var otherPairCard string 
			for card, count := range cardToCount {
				if count == 2 && card != "J" {
					otherPairCard = card
					break
				}
			}
			cardToCount[otherPairCard] = 4
			delete(cardToCount, "J")
			return cardToCount
		} else {  // J is the single; add to best pair
			bestPairCard := ""
			for card, _ := range cardToCount {
				if CARD_TO_VALUE_JOKER[card] > CARD_TO_VALUE_JOKER[bestPairCard] {
					bestPairCard = card
				}
			}
			cardToCount[bestPairCard] = 3
			delete(cardToCount, "J")
			return cardToCount
		}
	}

	if hand.isOnePair() {
		if cardToCount["J"] == 2 {
			bestCard := ""
			for card, _ := range cardToCount {
				if CARD_TO_VALUE_JOKER[card] >= CARD_TO_VALUE_JOKER[bestCard] {
					bestCard = card
				}
			}
			cardToCount[bestCard] = 3
			delete(cardToCount, "J")
			return cardToCount
		} else {
			var pairCard string
			for card, count := range cardToCount {
				if count == 2 {
					pairCard = card
					break
				}
			}
			cardToCount[pairCard] = 3
			delete(cardToCount, "J")
			return cardToCount
		}
	}

	if hand.isHighCard() {
		bestCard := ""
			for card, _ := range cardToCount {
				if CARD_TO_VALUE_JOKER[card] >= CARD_TO_VALUE_JOKER[bestCard] {
					bestCard = card
				}
			}
			cardToCount[bestCard] = 2
			delete(cardToCount, "J")
			return cardToCount
	}
	return cardToCount
}

func (hand Hand) getCardToCount(usingJokerRule bool) map[string]int {
	cardToCount := map[string]int{}
	for _, card := range hand.cards {
		card := string(card)
		if count, ok := cardToCount[card]; ok {
			cardToCount[card] = count + 1
		} else {
			cardToCount[card] = 1
		}
	}

	return hand.applyJokerRule(usingJokerRule, cardToCount)
}

func (hand Hand) isHighCard() bool {
	return len(hand.cardToCount) == 5
}

func (hand Hand) isOnePair() bool {
	cardToCount := hand.cardToCount
	if len(cardToCount) != 4 {
		return false
	}
	for _, count := range hand.cardToCount {
		if count != 1 && count != 2 {
			return false
		}
	}
	return true
}

func (hand Hand) isTwoPair() bool {
	cardToCount := hand.cardToCount
	if len(cardToCount) != 3 {
		return false
	}
	for _, count := range hand.cardToCount {
		if count != 1 && count != 2 {
			return false
		}
	}
	return true
}

func (hand Hand) isThreeOfAKind() bool {
	cardToCount := hand.cardToCount
	if len(cardToCount) != 3 {
		return false
	}
	for _, count := range hand.cardToCount {
		if count != 1 && count != 3 {
			return false
		}
	}
	return true
}

func (hand Hand) isFullHouse() bool {
	cardToCount := hand.cardToCount
	if len(cardToCount) != 2 {
		return false
	}
	for _, count := range hand.cardToCount {
		if count != 2 && count != 3 {
			return false
		}
	}
	return true
}

func (hand Hand) isFourOfAKind() bool {
	cardToCount := hand.cardToCount
	if len(cardToCount) != 2 {
		return false
	}
	for _, count := range hand.cardToCount {
		if count != 1 && count != 4 {
			return false
		}
	}
	return true
}

func (hand Hand) isFiveOfAKind() bool {
	return len(hand.cardToCount) == 1
}

func (hand Hand) GetValue() int {
	var isHandTypeFuncs []func() bool
	isHandTypeFuncs = append(  // ordered from worst hand to best hand
		isHandTypeFuncs,
		hand.isHighCard,
		hand.isOnePair,
		hand.isTwoPair,
		hand.isThreeOfAKind,
		hand.isFullHouse,
		hand.isFourOfAKind,
		hand.isFiveOfAKind,
	)
	for i, isHandType := range isHandTypeFuncs {
		if isHandType() {
			return i + 1  // +1 to reward value to lowest hand type
		}
	}
	return 0
}

func (hand1 Hand) TiebreakWinAgainst(hand2 Hand, usingJokerRule bool) bool {
	var cardToValue map[string]int
	if usingJokerRule {
		cardToValue = CARD_TO_VALUE_JOKER
	} else {
		cardToValue = CARD_TO_VALUE
	}

	for i := 0; i < 5; i++ {
		card1 := string(hand1.cards[i])
		card2 := string(hand2.cards[i])
		if cardToValue[card1] > cardToValue[card2] {
			return true
		} else if cardToValue[card1] < cardToValue[card2] {
			return false
		}
	}
	return true  // same card; so it doesn't really matter
}

func parseInput(usingJokerRule bool) ([]Hand, error) {
	pwd, err := os.Getwd()
	if err != nil {
		return nil, err
	}
	file, err := os.Open(pwd + "/dec_7/input.txt")
	if err != nil {
		return nil, err
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	var hands []Hand
	for scanner.Scan() {
		handAndBid := scanner.Text()
		cards := strings.Split(handAndBid, " ")[0]
		bidStr := strings.Split(handAndBid, " ")[1]
		bid, err := strconv.Atoi(bidStr)
		if err != nil {
			return nil, err
		}
		hands = append(hands, NewHand(cards, bid, usingJokerRule))
	}
	return hands, nil
}

func printAnswer(usingJokerRule bool) {
	hands, err := parseInput(usingJokerRule)
	if err != nil {
		log.Fatal(err)
	}

	sort.Slice(hands, func(i, j int) bool {
		hand1 := hands[i]
		hand2 := hands[j]
		if hand2.value > hand1.value {
			return true
		} else if hand2.value == hand1.value {  // break the tie
			return hand2.TiebreakWinAgainst(hand1, usingJokerRule)
		}
		return false

	}) // hands now sorted from lowest value to highest
	acc := 0
	for i, hand := range hands {
		rank := i + 1
		acc += hand.bid * rank
	}
	if !usingJokerRule {
		fmt.Println("Dec 7 part 1:", acc)
	} else {
		fmt.Println("Dec 7 part 2:", acc)
	}
}

func main() {
	printAnswer(false)
	printAnswer(true)
}
