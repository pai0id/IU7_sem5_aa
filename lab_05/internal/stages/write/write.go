package write

import (
	"context"
	"encoding/json"
	"fmt"
	"lab_05/internal/tasks"
	"log"

	"github.com/jackc/pgx/v4"
)

func WriteToDb(task *tasks.Task) error {
	conn, err := pgx.Connect(context.Background(), task.Context.Dsn)
	if err != nil {
		log.Fatalf("Unable to connect to database: %v", err)
	}
	defer conn.Close(context.Background())

	ingridients := make([][]byte, len(task.Data.Ingredients))

	for i := range ingridients {
		ingridients[i], err = json.Marshal(task.Data.Ingredients[i])
		if err != nil {
			return fmt.Errorf("failed to marshal ingredient %d: %w", i, err)
		}
	}

	query := `
		INSERT INTO recipies (id, url, title, ingredients, steps, image_url)
		VALUES ($1, $2, $3, $4, $5, $6)
		RETURNING id;
	`

	_, err = conn.Query(context.Background(), query,
		task.Data.Id,
		task.Data.Url,
		task.Data.Title,
		ingridients,
		task.Data.Steps,
		task.Data.ImageUrl,
	)
	if err != nil {
		return fmt.Errorf("failed to insert task.Data: %w", err)
	}

	return nil
}
