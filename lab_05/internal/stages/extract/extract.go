package extract

import (
	"lab_05/internal/tasks"
	"strings"
)

// func SplitStringByNumber(input string) (before string, number string, after string) {
// 	re := regexp.MustCompile(`(-?\d+(\.\d+)?)`)

// 	loc := re.FindStringIndex(input)
// 	if loc == nil {
// 		return input, "", ""
// 	}

// 	before = input[:loc[0]]
// 	number = input[loc[0]:loc[1]]
// 	after = input[loc[1]:]

// 	return before, number, after
// }

func SplitStringByNumber(input string) (before string, number string, after string) {
	start := -1
	end := -1

	for i, r := range input {
		if (r >= '0' && r <= '9') || r == '-' || r == '.' {
			if start == -1 {
				start = i
			}
		} else if start != -1 {
			end = i
			break
		}
	}

	if start != -1 && end == -1 {
		end = len(input)
	}

	if start == -1 {
		return input, "", ""
	}

	before = input[:start]
	number = input[start:end]
	after = input[end:]

	return before, number, after
}

func ParseText(task *tasks.Task) error {
	task.Data = tasks.Data{Id: task.ID}

	parts := strings.Split(task.Text, "\n\n")

	task.Data.Url = parts[0]
	task.Data.Title = parts[1]

	task.Data.Ingredients = make([]tasks.Ingredient, 0, 10)
	ingridients := strings.Split(parts[2], ";")
	for _, ing := range ingridients {
		name, unit, qty := SplitStringByNumber(ing)
		task.Data.Ingredients = append(task.Data.Ingredients, tasks.Ingredient{Name: name, Unit: unit, Quantity: qty})
	}

	task.Data.Steps = strings.Split(parts[3], "\n")
	task.Data.ImageUrl, _ = strings.CutPrefix(parts[4], "Image: ")
	return nil
}
