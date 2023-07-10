import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.Random;
import java.util.Scanner;
import java.util.Set;

/**
 * RA112649 - Thiago Yuji Yoshimura Yamamoto
 * RA102573 - Gabriel Henrique Costanzi
 */

class Vertice {
    public int identificador;
    public int x, y;
    public boolean visitado;

    public Vertice(){
        super();
    }

    public Vertice (int identificador, int x, int y){
        this.identificador = identificador;
        this.x = x;
        this.y = y;
    }

    public int calculaDistancia(Vertice verticeProximo){
        int x = verticeProximo.x - this.x;
        int y = verticeProximo.y - this.y;
        return (int) Math.sqrt(Math.pow(x,2) + Math.pow(y,2));
    }
}

class Caminho implements Comparable{
    ArrayList<Vertice> caminho = new ArrayList<Vertice>();
    int fitness;

    public void calcula_fitness(){
        this.fitness = 0;
        for(int i = 0; i < this.caminho.size()-1; i++) this.fitness = this.fitness + this.caminho.get(i).calculaDistancia(this.caminho.get(i+1));
        this.fitness = this.fitness + this.caminho.get(this.caminho.size()-1).calculaDistancia(this.caminho.get(0));
    }

    @Override
    public int compareTo(Object comparestu){
        int compare_fitness=((Caminho)comparestu).fitness;
        return this.fitness-compare_fitness;
    }

}

class Main {
    private static void swap2OPT(Caminho saidaOPT, int verticeB, int i){
        Collections.swap(saidaOPT.caminho, verticeB, i);
        int a = verticeB+1;
        int b = i-1;
        while(a < b){
            Collections.swap(saidaOPT.caminho, a, b);
            a++;
            b--;
        }
    }

    private static void melhorativo2OPT(Caminho individuo, ArrayList<Caminho> nova_populacao, int busca_local_profundidade){
        //Algoritmo Melhorativo 2-OPT
        boolean temOPT = true;
        Caminho individuo_OPT = new Caminho();
        individuo_OPT.caminho.addAll(individuo.caminho);
        int melhoraAB = 0;
        int paradaAB = individuo_OPT.caminho.size()-1;

        while(temOPT && (busca_local_profundidade--) > 0){
            temOPT = false;
            paradaAB = individuo_OPT.caminho.size()-1;
            for(int verticeA = melhoraAB; verticeA < paradaAB && !temOPT; verticeA++){
                if(melhoraAB > 0 && verticeA == individuo_OPT.caminho.size()-2){
                    paradaAB = melhoraAB;
                    verticeA = 0;
                }
                int verticeB = verticeA + 1;
                for(int i = verticeB+1; i < individuo_OPT.caminho.size()-1 && !temOPT; i++){
                    int j = i+1;
                    if(j != verticeA){
                        int menor = individuo_OPT.caminho.get(verticeA).calculaDistancia(individuo_OPT.caminho.get(verticeB)) + individuo_OPT.caminho.get(i).calculaDistancia(individuo_OPT.caminho.get(j));
                        int custo = (individuo_OPT.caminho.get(verticeA).calculaDistancia(individuo_OPT.caminho.get(i)) + individuo_OPT.caminho.get(verticeB).calculaDistancia(individuo_OPT.caminho.get(j)));
                        if(custo < menor){  
                            swap2OPT(individuo_OPT, verticeB, i);     
                            temOPT = true;
                            melhoraAB = verticeA;
                        }   
                    
                    }
                }
            }
        }   

        individuo_OPT.calcula_fitness();
        
        nova_populacao.add(individuo_OPT);
        
    }

    //Criação das tabelas em .txt de cada combinação dos algoritmos
    //Utilizamos o arquivo para gerar um gráfico no excel e apresenta-lo no relatório
    private static PrintWriter cria_tabela(String nomeArquivo){
        try{
            FileWriter leitor = new FileWriter("./tabelas/".concat(nomeArquivo.concat(".txt")));
            PrintWriter bufferWriter = new PrintWriter(leitor, true);
            bufferWriter.println("Geracao,Melhor_Geracao,Pior_Geracao,Melhor_Geral");
            return bufferWriter;
        }catch(IOException ex){
            System.out.println("Falha na leitura do arquivo");
            System.exit(0);
            return null;
        }
    }

    //Retorna a lista selecionada, usada para conseguir usar um for nas funções operadores
    private static Caminho select_list(int i, Caminho individuo_1, Caminho individuo_2){
        if(i == 1) return individuo_1;
        else return individuo_2;
    }
   
    //Cria um array com n números randomicos diferentes em um intervalo de 0 a list_size
    private static ArrayList<Integer> n_random_numbers(int n, int list_size){
        Random random = new Random();
        Set<Integer>buffer = new LinkedHashSet<Integer>();
        while (buffer.size() < n) {
            buffer.add(random.nextInt(list_size));
        }
        ArrayList<Integer> posicao_array = new ArrayList<Integer>(buffer);
        return posicao_array;

    }
 
    //Algoritmo Construtivo Vizinho mais próximo, servirá como método para a criação da população inicial
    private static Caminho construtivo_vizinho_proximo(ArrayList<Vertice> listVertice){   
        /**Inicializa:
         * i --> qual vertice começara (gerado o valor aleatoriamente de acordo com a quantidade de vértices)
         * menor --> menor peso do vértice (da posição i na lista) para o j
         */
        Caminho cromossomo = new Caminho();
        int menor = Integer.MAX_VALUE;
        int menorB = 0;     
        int A = new Random().nextInt(listVertice.size());
        Vertice vertice = listVertice.get(A);
        Vertice verticeProximo = new Vertice();
        listVertice.remove(A);
        cromossomo.caminho.add(vertice);
        while(!listVertice.isEmpty()){
            for(int B = 0; B < listVertice.size(); B++){
                verticeProximo = listVertice.get(B);
                int peso = vertice.calculaDistancia(verticeProximo);
                if(peso < menor){
                    menor = peso;
                    menorB = B;
                }               
            }
            vertice = listVertice.get(menorB);
            cromossomo.caminho.add(vertice);           
            listVertice.remove(menorB);
            menor = Integer.MAX_VALUE;
        }
        //cromossomo.caminho.add(cromossomo.caminho.get(0));
        cromossomo.calcula_fitness();

        return cromossomo;
    }

    //Seleção dos indivíduos a partir da técnica do selecao_torneio
    //Dentre k indivíduos aleatórios da população selecione o que houver melhor fitness
    private static Caminho selecao_roleta(ArrayList<Caminho> populacao){
        double total = 0;
        double anterior = 0;
        int i = 0;

        for (i = 0; i < populacao.size(); i++) total = total + populacao.get(i).fitness;

        double seleciona = Math.random();
        //System.out.println(seleciona);
        int index = 0;
        
        for (i = 0; i < populacao.size(); i++) {
            double pedaco = (total - populacao.get(i).fitness) / (total * populacao.size());    
            anterior += pedaco;
            if(anterior >= seleciona){
                index = i;
                break;
            }
        } 
        //System.out.println("index: " + index);
        //System.out.println(index);
        Caminho buffer = populacao.get(index);
        populacao.remove(index);
        return buffer;
    }

    //Operador de Cruzamento Ox1 --> produz 2 filhos a partir de 2 pais
    private static void operador_Ox1(ArrayList<Caminho> nova_populacao, Caminho pai_1, Caminho pai_2){
        Caminho filho_1 = new Caminho();
        Caminho filho_2 = new Caminho();
        int i , j ;
        
        j = (int) Math.round(Math.random() * (pai_1.caminho.size() - 2)) + 1;
        i = (int) Math.round((Math.random() * (j - 1)))+1;
        
        

        for(int k = 1; k <= 2; k++){
            ArrayList<Vertice> intervalo = new ArrayList<Vertice>();
            Caminho filho_k = select_list(k, filho_1, filho_2);
            for (int l = 0; l < pai_1.caminho.size(); l++) {
                filho_k.caminho.add(l, new Vertice());
            }
            for (int l = i; l < j+1; l++) {
                filho_k.caminho.set(l, select_list(k, pai_1, pai_2).caminho.get(l));
            }
            int idx = j+1;
            Vertice cidade = select_list((k % 2) + 1, pai_1, pai_2).caminho.get(j);
            while (idx != i){
                
                if (idx >  select_list((k % 2) + 1, pai_1, pai_2).caminho.size()-1){
                    idx = 0;
                }
                while (filho_k.caminho.contains(cidade)){     
                    int aux = select_list((k % 2) + 1, pai_1, pai_2).caminho.indexOf(cidade);
                    if(aux == select_list((k % 2) + 1, pai_1, pai_2).caminho.size()-1){
                        cidade = select_list((k % 2) + 1, pai_1, pai_2).caminho.get(0);
                    }
                    else{
                        cidade = select_list((k % 2) + 1, pai_1, pai_2).caminho.get(aux+1);
                        
                    }
                }
                filho_k.caminho.set(idx, cidade);
                idx++;
            }          
            filho_k.calcula_fitness();
            
            //System.out.println("fitness: "+ filho_k.fitness);
            //System.out.println("Filho: " + filho_k.fitness);
            nova_populacao.add(filho_k);
        }
        
    }

    //Operador de Cruzamento Ox2 --> produz 2 filhos a partir de 2 pais
    private static void operador_Ox2(ArrayList<Caminho> nova_populacao, int quantidade_posicoes, Caminho pai_1, Caminho pai_2){
        Caminho filho_1 = new Caminho();
        Caminho filho_2 = new Caminho();

        for(int i = 1; i <= 2; i++){
            ArrayList<Integer> posicao_array = n_random_numbers(quantidade_posicoes, (select_list((i % 2) + 1, pai_1, pai_2).caminho.size()));
            
            Caminho filho_i = select_list(i, filho_1, filho_2);
            filho_i.caminho.addAll(select_list(i, pai_1, pai_2).caminho);
            
            ArrayList<Integer> conteudo_array = new ArrayList<Integer>();

            for(int j = 0; j < posicao_array.size(); j++){
                conteudo_array.add(select_list(i,pai_1, pai_2).caminho.indexOf(select_list((i % 2) + 1, pai_1, pai_2).caminho.get(posicao_array.get(j))));
            }

            Collections.sort(conteudo_array);

            for(int k = 0; k < conteudo_array.size(); k++){
                //System.out.println("k = " + conteudo_array.get(k));
                filho_i.caminho.set(conteudo_array.get(k), select_list((i % 2) + 1, pai_1, pai_2).caminho.get(posicao_array.get(k)));
            }

            filho_i.calcula_fitness();
            
            nova_populacao.add(filho_i);
        }

        // System.out.println("Filho1: ");
        // filho_1.caminho.forEach((vertice) -> System.out.print(vertice.identificador + " -> "));
        // System.out.println("\nFilho2: ");
        // filho_2.caminho.forEach((vertice) -> System.out.print(vertice.identificador + " -> "));
    }

    
    //Mutação de um indivíduo a partir da troca dos valores de duas posições
    private static void gerar_mutacao(ArrayList<Caminho> populacao){
        int i = new Random().nextInt(populacao.size());

        Caminho individuo_mutacao = new Caminho();
        individuo_mutacao.caminho.addAll(populacao.get(i).caminho);

        ArrayList<Integer> posicao_array = n_random_numbers(2, populacao.get(i).caminho.size());

        Collections.swap(individuo_mutacao.caminho, posicao_array.get(0), posicao_array.get(1));
        individuo_mutacao.calcula_fitness();

        populacao.add(individuo_mutacao);
    }

    //Etapa Criação da população inicial
    private static ArrayList<Caminho> etapa_populacao_inical(int tamanho_populacao_inicial, ArrayList<Vertice> listVertice){
        ArrayList<Caminho> populacao = new ArrayList<Caminho>();
        for (int i = 0; i < tamanho_populacao_inicial; i++) {
            populacao.add(construtivo_vizinho_proximo(new ArrayList<Vertice>(listVertice)));
        }
        return populacao;
    }
    
    //Etapa Calculo de aptidão, função objetiva do problema do caixeiro viajante é a minimização do peso do caminho
    private static void etapa_1_aptidao(ArrayList<Caminho> populacao){
        Collections.sort(populacao);
    }

    //Etapa Seleção dos cromossomos a serem cruzados
    private static ArrayList<Caminho> etapa_2_selecao(double taxa_cruzamento, ArrayList<Caminho> populacao){
        ArrayList<Caminho> selecao_populacao = new ArrayList<Caminho>();
        ArrayList<Caminho> buffer_populacao = new ArrayList<Caminho>(populacao);

        int quantidade_cromossomos = (int) (buffer_populacao.size() * taxa_cruzamento);

        quantidade_cromossomos = quantidade_cromossomos +(quantidade_cromossomos % 2);

        while(selecao_populacao.size() < quantidade_cromossomos){
            selecao_populacao.add(selecao_roleta(buffer_populacao));
        }
        
        return selecao_populacao;
    }

    //Etapa Cruzamento dos cromossomos selecionados da etapa 2
    private static ArrayList<Caminho> etapa_3_cruzamento(String operador, ArrayList<Caminho> populacao, ArrayList<Caminho> selecao_populacao, int quantidade_posicoes){
        ArrayList<Caminho> nova_populacao = new ArrayList<Caminho>();
        for (int i = 0; i < selecao_populacao.size()-1; i++) {
            if(operador.equals("OX2")){
                operador_Ox2(nova_populacao, quantidade_posicoes, selecao_populacao.get(i), selecao_populacao.get(i+1));
            }else{
                operador_Ox1(nova_populacao, selecao_populacao.get(i), selecao_populacao.get(i+1));
            }
        }

        return nova_populacao;
    }

    //Etapa Mutação de um dos indivíduos da nova população
    private static void etapa_4_mutacao(ArrayList<Caminho> nova_populacao, double taxa_mutacao){
        double probabilidade = Math.random();

        if(probabilidade <= taxa_mutacao){
            gerar_mutacao(nova_populacao);
        }
    }

    //Etapa Busca Local para gerar novos vizinhos - 2-OPT
    private static void etapa_5_busca_local(ArrayList<Caminho> populacao, ArrayList<Caminho> nova_populacao, double taxa_busca_local, int busca_local_profundidade){
        int n_individuos_populacao = (int) (nova_populacao.size() * taxa_busca_local);
        
        for (int i = 0; i < n_individuos_populacao; i++) {
            melhorativo2OPT(nova_populacao.get(i), nova_populacao, busca_local_profundidade);
        }     
    }

    //Etapa Atualização da população com os novos individuos
    private static void etapa_6_atualizacao(ArrayList<Caminho> populacao, ArrayList<Caminho> nova_populacao, double taxa_sobrevivencia){
        Collections.sort(nova_populacao);

        int n_individuos_populacao = (int) (populacao.size() * taxa_sobrevivencia);

        int j = 0;
        int inicio = n_individuos_populacao;

        for (int i = inicio; i < populacao.size() && i < nova_populacao.size(); i++) {
            populacao.set(i,nova_populacao.get(j++));
        }
    }

    //Algoritmo Genético
    private static void algoritmo_genetico(String operador,
        PrintWriter bufferWriter, int max_geracoes, int tamanho_populacao,
        int posicoes_cruzamento, int busca_local_profundidade, double taxa_busca_local,
        double taxa_cruzamento, double taxa_mutacao, double taxa_sobrevivencia,
        ArrayList<Vertice> listVertice, double melhor_resultado
        ){
        try{
            String condicao_parada = "";
            int geracao = 0;
            int estagnacao = (int) (0.3 * max_geracoes);
            int diferenca_geracao_melhoria = 0;
            System.out.println("Construindo população inicial...");

            ArrayList<Caminho> populacao = etapa_populacao_inical(tamanho_populacao, listVertice);

            int caminho_entrada = populacao.get(0).fitness;

            int anterior = caminho_entrada;

            System.out.println("Iniciando algoritmo genético com operador " + operador + "...");

            long inicio = System.currentTimeMillis();
            long fim = 0;
            
            while(diferenca_geracao_melhoria < estagnacao && (fim - inicio) < 9000000 && (geracao < max_geracoes)){
                diferenca_geracao_melhoria++;
                etapa_1_aptidao(populacao);
                System.out.println("Geração " + geracao + " melhor: " + populacao.get(0).fitness);
                System.out.println("Geração " + geracao + " pior: " + populacao.get(populacao.size()-1).fitness);

                ArrayList<Caminho> selecao_populacao = etapa_2_selecao(taxa_cruzamento, populacao);
                
                ArrayList<Caminho> nova_populacao = etapa_3_cruzamento(operador, populacao, selecao_populacao, posicoes_cruzamento);

                etapa_4_mutacao(nova_populacao, taxa_mutacao);

                etapa_5_busca_local(populacao, nova_populacao, taxa_busca_local, busca_local_profundidade);

                etapa_6_atualizacao(populacao, nova_populacao, taxa_sobrevivencia);

                etapa_1_aptidao(populacao);

                if(populacao.get(0).fitness < anterior){
                    diferenca_geracao_melhoria = 0;
                    System.out.println("Geração " + geracao + ": " + populacao.get(0).fitness);
                }      
                
                anterior = populacao.get(0).fitness;

                bufferWriter.println(geracao + "," + nova_populacao.get(0).fitness + "," + nova_populacao.get(nova_populacao.size()-1).fitness + "," + populacao.get(0).fitness);
                geracao++;
                fim = System.currentTimeMillis();
            }  
            double precisao = melhor_resultado/populacao.get(0).fitness;
            if(geracao == max_geracoes) {
                condicao_parada = "MAX_GERACAO";
            }else if(diferenca_geracao_melhoria == estagnacao){
                condicao_parada = "ESTAGNACAO";
            }else if((fim - inicio) >= 9000000){
                condicao_parada = "TEMPO_ESGOTADO";
            }
            System.out.println("----------------------------------------------");
            System.out.println("Melhor individuo -> População inicial:");
            System.out.println("Fitness: " + caminho_entrada);
            System.out.println("Melhor individuo -> População Geração " + geracao + ":");
            System.out.println("Fitness: " + populacao.get(0).fitness);
            System.out.println("Precisão: " + precisao);
            System.out.println("Condição de parada atendida: " + condicao_parada);
            System.out.println("----------------------------------------------"); 
            bufferWriter.println("\nPrecisao,Condicao_Parada,Tempo,Melhor_Fitness");
            bufferWriter.println(precisao + "," + condicao_parada + "," + ((fim - inicio)/1000) + "," + populacao.get(0).fitness);
            bufferWriter.println("\ntamanho_populacao,posicoes_cruzamento,busca_local_profundidade,taxa_busca_local,taxa_cruzamento,taxa_mutacao,taxa_sobrevivencia");
            bufferWriter.println(tamanho_populacao + "," + posicoes_cruzamento + "," + busca_local_profundidade + "," + taxa_busca_local + "," + taxa_cruzamento + "," + taxa_mutacao + "," + taxa_sobrevivencia);
        }catch(Exception e){
            System.out.println("Erro inesperado: " + e.toString());
        }finally{
            bufferWriter.close();
        }     

    }

    public static void main(String[] args) throws Exception {              
        ArrayList<Vertice> listVertice = new ArrayList<Vertice>();
        HashMap<String,Double> resultado = new HashMap<String,Double>();

        String operador = args[0];
        String entrada = args[1];
        int tamanho_populacao = Integer.parseInt(args[2]);
        int posicoes_cruzamento = Integer.parseInt(args[3]);
        int busca_local_profundidade = Integer.parseInt(args[4]);
        double taxa_busca_local = Double.parseDouble(args[5]);
        double taxa_cruzamento = Double.parseDouble(args[6]);
        double taxa_mutacao = Double.parseDouble(args[7]);
        double taxa_sobrevivencia = Double.parseDouble(args[8]);
        
        Scanner readerOtimo = new Scanner(new FileReader("./resultados.txt"));
        Scanner reader = new Scanner(new FileReader("./entradas/".concat(entrada.concat(".tsp"))));

        //Leitura do arquivo resultados.txt, para calcular a precisão dos algoritmos
        while(readerOtimo.hasNextLine()){
            String[] linha = readerOtimo.nextLine().split("[:]");
            resultado.put(linha[0],Double.parseDouble(linha[1]));
        }
        readerOtimo.close();

        //Pula a leitura das 6 primeiras linhas
        while(!reader.hasNextInt()) reader.nextLine();
        
        while(reader.hasNextInt()){
            int identificador;
            int x, y;

            identificador = reader.nextInt();
            x = reader.nextInt();
            y = reader.nextInt();

            listVertice.add(new Vertice(identificador, x, y));
        }

        reader.close();

        int max_geracoes = 1000;

        switch(operador){
            case "-ox2":
                //Execução do algoritmo genético com operador OX2
                algoritmo_genetico("OX2",
                    cria_tabela(entrada.concat("_OX2")), max_geracoes, tamanho_populacao,
                    posicoes_cruzamento, busca_local_profundidade, taxa_busca_local,
                    taxa_cruzamento, taxa_mutacao, taxa_sobrevivencia,
                    new ArrayList<Vertice>(listVertice), resultado.get(entrada));
                break;
            case "-ox1":
                //Execução do algoritmo genético com operador OX1
                algoritmo_genetico("OX1",
                    cria_tabela(entrada.concat("_OX1")), max_geracoes, tamanho_populacao,
                    posicoes_cruzamento, busca_local_profundidade, taxa_busca_local,
                    taxa_cruzamento, taxa_mutacao, taxa_sobrevivencia,
                    new ArrayList<Vertice>(listVertice), resultado.get(entrada));
                break;
            default:
                System.out.println("Operador '" + operador + "' não existe, utilize -ox1 ou -ox2");
                break;
        }
    
    }
}