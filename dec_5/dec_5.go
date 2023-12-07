package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

// Represents
type RangeMap struct {
	destStart int
	srcStart  int
	rangeLen  int
}

func parseRangeMap(mappingStr []string) []RangeMap {
	var mapping []RangeMap
	for _, mapLine := range mappingStr {
		values := strings.Split(mapLine, " ")
		destStart, _ := strconv.Atoi(values[0])
		srcStart, _ := strconv.Atoi(values[1])
		rangeLen, _ := strconv.Atoi(values[2])

		mapping = append(mapping, RangeMap{destStart, srcStart, rangeLen})
	}
	sort.Slice(mapping, func(i, j int) bool {
		return mapping[i].srcStart < mapping[j].srcStart
	})
	return mapping
}

func convertNumber(number int, mapping []RangeMap) int {
	left := 0
	right := len(mapping) - 1

	// binary search for the correct range
	for left <= right {
		mid := left + (right - left) / 2
		mapRange := mapping[mid]

		if number >= mapRange.srcStart && number < mapRange.srcStart + mapRange.rangeLen {
			return mapRange.destStart + (number - mapRange.srcStart)
		} else if number < mapRange.srcStart {
			right = mid - 1
		} else {
			left = mid + 1
		}
	}

	return number // return the number itself if no mapping is found
}

func parseInput() ([]string, [][]RangeMap) {
	pwd, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}
	file, err := os.Open(pwd + "/dec_5/input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var seeds []string
	var maps [][]RangeMap
	var currentMap []string

	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			if len(currentMap) > 0 {
				maps = append(maps, parseRangeMap(currentMap))
				currentMap = nil
			}
		} else if strings.Contains(line, "seeds") {
			seedsStr := strings.Split(line, ": ")[1]
			seeds = strings.Split(seedsStr, " ")
		} else if strings.Contains(line, "map:") {
			currentMap = []string{}
		} else {
			currentMap = append(currentMap, line)
		}
	}

	if len(currentMap) > 0 {
		maps = append(maps, parseRangeMap(currentMap))
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return seeds, maps
}

func getAnswerPart1(seeds []string, maps [][]RangeMap) int {
	minLocation := -1

	for _, seedStr := range seeds {
		seed, _ := strconv.Atoi(seedStr)
		currentNum := seed

		for _, mapping := range maps {
			currentNum = convertNumber(currentNum, mapping) // step thru all mappings
		}

		if minLocation == -1 || currentNum < minLocation {
			minLocation = currentNum
		}
	}

	return minLocation
}

// Finding the lowest location number of pt.2 using goroutines and ranges
func getAnswerPart2(seeds []string, maps [][]RangeMap) int {
	var wg sync.WaitGroup
	results := make(chan int)

	for i := 0; i < len(seeds); i += 2 {
		start, _ := strconv.Atoi(seeds[i])
		length, _ := strconv.Atoi(seeds[i+1])
		wg.Add(1)

		go func(start, length int) {
			defer wg.Done()
			for j := 0; j < length; j++ {
				seed := start + j
				currentNum := seed
				for _, mapping := range maps {
					currentNum = convertNumber(currentNum, mapping)
				}
				results <- currentNum
			}
		}(start, length)
	}

	go func() {
		wg.Wait()
		close(results)
	}()

	minLocation := -1
	for currentNum := range results {
		if minLocation == -1 || currentNum < minLocation {
			minLocation = currentNum
		}
	}

	return minLocation
}

func main() {
	seeds, maps := parseInput()
	lowestLocation := getAnswerPart1(seeds, maps)
	fmt.Println("Dec 5 Part 1:", lowestLocation)

	start := time.Now()
	fmt.Print("This might take a couple minutes... Brute force xd")
	lowestLocation = getAnswerPart2(seeds, maps)
	duration := time.Since(start)
	fmt.Printf("Dec 5 Part 2: %d. Time taken: %s\n", lowestLocation, duration)
}
