package read

import (
	"lab_05/internal/tasks"
	"os"
)

func ReadFileToString(task *tasks.Task) error {
	data, err := os.ReadFile(task.FileName)
	if err != nil {
		return err
	}
	task.Text = string(data)
	return nil
}
