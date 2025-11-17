// *******************************************************
// Inside the baseTEST_LED.h
// *******************************************************


// =========================================
// Main Functions
// =========================================

void toggleLightTEST(void);

void initialLED_TEST(int v);



// =========================================
// GPIO Initialization
// =========================================

void btLED_GPIO_Init(void);

// User Button PC13
void UB_GPIO_Init(void);

// LED PA5
void InternalLED_GPIO_Init(void);


// *******************************************************
// Inside the baseTEST_LED.c
// *******************************************************
// HEADER
#include "baseTest_LED.h"


// =========================================
// Main Functions
// =========================================


void toggleLightTEST(void)
{
	// User Button PC13
	GPIO_PinState buttonState = HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13);
	if (buttonState == GPIO_PIN_RESET){
		HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5); // Toggle LED
        HAL_Delay(200); // 200ms
	}
}

void initialLED_TEST(int v){
	// 0: off, 1: on

	if (v == 0){
		HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET); // Turn OFF
	}
	else if (v == 1){
		HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET); // Turn OFF
	}
}


// =========================================
// GPIO Initialization
// =========================================


void btLED_GPIO_Init(void){
	UB_GPIO_Init();
	InternalLED_GPIO_Init();
}


// User Button PC13
void UB_GPIO_Init(void){
	__HAL_RCC_GPIOC_CLK_ENABLE();  // Enable GPIOC clock
	GPIO_InitTypeDef GPIO_InitStruct = {0};

    // Configure PC13 as input (Button)
    GPIO_InitStruct.Pin = GPIO_PIN_13;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
}


// Internal LED PA5
void InternalLED_GPIO_Init(void){
	__HAL_RCC_GPIOA_CLK_ENABLE();  // Enable GPIOA clock
	GPIO_InitTypeDef GPIO_InitStruct = {0};

    // Configure PA5 as output (LED)
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;  // Push-pull output
    GPIO_InitStruct.Pull = GPIO_NOPULL;          // No internal pull-up or pull-down
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}


// *******************************************************
// Inside the main.h file
// *******************************************************



// For TEST
#include "baseTest_LED.h"


// *******************************************************
// Inside the main.c file
// with sysClock setup
// *******************************************************

int main(void)
{

  HAL_Init();
  SystemClock_Config();

  btLED_GPIO_Init();

  // LED set up
  initialLED_TEST(0);

  while (1)
  {
  	toggleLightTEST();
  }
}
